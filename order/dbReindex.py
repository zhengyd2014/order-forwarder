
import pyodbc
from datetime import datetime
import uuid
from order import util, config
import logging
import win32com.client
import os
from shutil import copyfile
import time


class DbReindexer:
    def __init__(self, dbFile):
        
        (path, filename) = os.path.split(os.path.abspath(dbFile))
        (root, extenstion) = os.path.splitext(filename)
        time_string = time.strftime("%Y%m%dT%H%M%S", time.localtime())

        self.compactedDBFile = f"{path}\{root}-reindexed-{time_string}{extenstion}"
        temp_db_file = f"{path}\{root}-temp-{time_string}{extenstion}"
        copyfile(dbFile, temp_db_file)
        self.orignalDBFile = temp_db_file
        

    def get_connection(self, dbFile):
        connectionStr = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' + f'DBQ={dbFile};'
        print(f"create connection with connectStr: {connectionStr}")
        conn = pyodbc.connect(connectionStr)
        return conn

    
    def delete_all_records_for_table(self, conn, tableName):
        cursor = conn.cursor()
        cursor.execute(f'delete from {tableName}')
        cursor.close()
        conn.commit()


    def compact(self, dbFile):
        srcDB = dbFile

        (path, filename) = os.path.split(os.path.abspath(dbFile))
        (root, extenstion) = os.path.splitext(filename)
        
        destDB = f"{path}\{root}-dest{extenstion}"

        oApp = win32com.client.Dispatch("Access.Application")
        oApp.compactRepair(srcDB, destDB)
        oApp.Application.Quit()
        oApp = None

        os.remove(srcDB)
        os.rename(destDB, srcDB)


    def reindex(self):
        
        # 1. make a new compacted copy of the db
        #    1.1: delete all records in OrderTranstions and OrderVoidLogs tables
        #    1.2: do a compact and repair
        copyfile(self.orignalDBFile, self.compactedDBFile)
        compacted_db_conn = self.get_connection(self.compactedDBFile)
        self.delete_all_records_for_table(compacted_db_conn, "OrderTransactions")
        self.delete_all_records_for_table(compacted_db_conn, "OrderVoidLogs")
        compacted_db_conn.close()

        self.compact(self.compactedDBFile)
        logging.info("created compacted db file with empty records in OrderTranstions and OrderVoidLogs tables")

        #
        # 3. OrignalDB - OrderTransactions / OrderVoidLogs table: cleanup 
        #    3.1: delete all records when their TransactionStatus == 5 in OrderTransactions table
        #    3.2: delete records accordingly in OrderVoidLogs table for above records
        original_db_conn = self.get_connection(self.orignalDBFile)
        original_db_cursor = original_db_conn.cursor()
        original_db_cursor.execute('select * from OrderTransactions where TransactionStatus = ?', 5)
        records_with_status_5 = original_db_cursor.fetchall()
        
        logging.info(f"find {len(records_with_status_5)} order transactions with transaction status == 5")
        for orderTransaction in records_with_status_5:
            orderTransactionID = orderTransaction.OrderTransactionID
            original_db_cursor.execute('delete from OrderVoidLogs where OrderTransactionID = ?', orderTransactionID)
            original_db_cursor.execute('delete from OrderTransactions where OrderTransactionID = ?', orderTransactionID)
            logging.info(f"deleted record with OrderTransactionID: {orderTransactionID}")

        logging.info(f"clean up records in original db, removed all the 'TransactionStatus == 5' records, number: {len(records_with_status_5)}")

        #
        # 4. CompactedDB - OrderTransactions table:
        #
        original_db_cursor.execute('select * from OrderTransactions order by OrderTransactionID')
        order_transactions = original_db_cursor.fetchall()
        logging.info(f"backfilling records for OrderTransactions table, number: {len(order_transactions)}")

        order_transactions_col_names = [x[0] for x in original_db_cursor.description]
        compacted_db_conn = self.get_connection(self.compactedDBFile)
        compacted_db_cursor = compacted_db_conn.cursor()
        reconcile_count = 0
        void_record_in_order_transactions_table = 0

        #  4.1 fill up OrderTransactions table with records from originalDB one by one
        for order_transaction in order_transactions:
            
            # insert into compactedDB OrderTransactions table
            row_as_dict = dict(zip(order_transactions_col_names, order_transaction))
            del row_as_dict["OrderTransactionID"]
            (insertStatement, valueList) = util.buildInsertStatement("OrderTransactions", row_as_dict)
    
            # logging.info(f"statement: {insertStatement}")
            # logging.info(f"values: {valueList}")
            compacted_db_cursor.execute(insertStatement, valueList)
            
            # 4.2 for records when "TransactionStatus == 2" do one additional thing:
            #     update originalDB OrderVoidLogs table with the new OrderTransactionID
            if order_transaction.TransactionStatus == "2":
                void_record_in_order_transactions_table += 1
                new_id = self.findOrderTransactionID(order_transaction.RowGUID, compacted_db_conn)
                old_id = order_transaction.OrderTransactionID
                logging.info(f"--- {old_id} ---")
                logging.info(f'found one OrderTransaction record with "TransactionStatus == 2", {old_id} (old) -> {new_id} (new)')
                original_db_cursor.execute("select * from OrderVoidLogs where OrderTransactionID = ?", old_id)
                void_log = original_db_cursor.fetchone()
                if void_log is None:
                    logging.warn(f"no corresponding record found in OrderVoidLogs with OrderTransactionID: {old_id}, skip reconciliation")
                else:
                    original_db_cursor.execute(
                        'update OrderVoidLogs set OrderTransactionID = ? where AutoID = ?',
                        new_id, 
                        void_log.AutoID)
                    logging.info(f"reconciled a VoidLog record: OrderID: {order_transaction.OrderID}, OrderTransactionID: {old_id}(old) -> {new_id}(new)")
                    reconcile_count += 1

        

        #
        # 5. CompactedDB - OrderVoidLogs table:
        #    fill up OrderVoidLogs table one by one
        original_db_cursor.execute('select * from OrderVoidLogs')
        void_logs = original_db_cursor.fetchall()


        void_logs_col_names = [x[0] for x in original_db_cursor.description]
        for void_log in void_logs:
            row_as_dict = dict(zip(void_logs_col_names, void_log))
            del row_as_dict["AutoID"]
            (insertStatement, valueList) = util.buildInsertStatement("OrderVoidLogs", row_as_dict)
            compacted_db_cursor.execute(insertStatement, valueList)

        #
        # 6. replace the originalDB with the compactedDB
        original_db_conn.commit()
        compacted_db_conn.commit()
        original_db_conn.close()
        compacted_db_conn.close()

        os.remove(self.orignalDBFile)

        logging.info(" ")
        logging.info("====== Summary ========")
        logging.info(f"deleted {len(records_with_status_5)} records from OrderTransactions for with 'TransactionStatus == 5'")
        logging.info(f"moved {len(order_transactions)} records from original db to compacted db for OrderTransactions table")
        logging.info(f"found {void_record_in_order_transactions_table} records with 'TransactionStatus == 2'")
        logging.info(f"reconciled {reconcile_count} records in original OrderVoidLogs table")
        logging.info(f"moved {len(void_logs)} records from original db to compacted db for OrderVoidLogs table")
        logging.info(" ")
        logging.info(f"**** the newly reindexed db file at: {self.compactedDBFile} ****")


    def findOrderTransactionID(self, rowUUID, conn):
        cursor = conn.cursor()
        cursor.execute('select * from OrderTransactions where RowGUID = ?', rowUUID)
        row = cursor.fetchone()
        cursor.close()
        return row.OrderTransactionID
