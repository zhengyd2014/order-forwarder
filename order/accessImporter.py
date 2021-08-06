
import pyodbc
from datetime import datetime
import uuid
from order import util, config

class AccessImporter:
    def __init__(self, dbFile):
        # self.conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=Y:\new-01-16.mdb;')
        connectionStr = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' + f'DBQ={dbFile};'
        # print(f"connectStr: {connectionStr}")
        self.conn = pyodbc.connect(connectionStr)


    def close(self):
        print("close database connection")
        self.conn.close()

 
    def printAllRows(self, tableName):
        cursor = self.conn.cursor()
        cursor.execute(f'select * from {tableName}')
        for row in cursor.fetchall():
            print (row)
        
        cursor.close()


    def displayMenuItems(self):
        cursor = self.conn.cursor()
        cursor.execute(f'select MenuItemID, MenuItemText, SecLangMenuItemText from MenuItems')
        for row in cursor.fetchall():
            print (row)
        
        cursor.close()

    def printAllTables(self):
        cursor = self.conn.cursor()
        for row in cursor.tables():
            print(row)

        cursor.close()
 

    def describeTable(self, tableName):
        cursor = self.conn.cursor()
        cursor.execute(f'select * from {tableName}')
        for col in cursor.description:
            print(f'\tcol: {col}')
        cursor.close()
 
    def importOrder(self, order):
        orderId = self.insertOrderHeaders(order)
        for orderItem in util.getObjectField(order, "orderItems", []):
            self.insertOrderTransactions(orderId, orderItem)

        self.insertSurchargeInOrderTransactions(orderId)


    # insert into OrderTransactions
    '''
        col: ('OrderTransactionID', <class 'int'>, None, 10, 10, 0, False)
        col: ('OrderID', <class 'int'>, None, 10, 10, 0, True)
        col: ('MenuItemID', <class 'int'>, None, 10, 10, 0, True)
        col: ('MenuItemAutoPriceText', <class 'str'>, None, 6, 6, 0, True)
        col: ('MenuItemUnitPrice', <class 'float'>, None, 24, 24, 0, True)
        col: ('Quantity', <class 'float'>, None, 24, 24, 0, True)
        col: ('ExtendedPrice', <class 'float'>, None, 24, 24, 0, True)
        col: ('DiscountID', <class 'int'>, None, 10, 10, 0, True)
        ...
        col: ('TransactionStatus', <class 'str'>, None, 1, 1, 0, True)
        col: ('NotificationStatus', <class 'str'>, None, 1, 1, 0, True)
        col: ('Mod1ID', <class 'int'>, None, 10, 10, 0, True)
        col: ('Mod1Cost', <class 'float'>, None, 24, 24, 0, True)
        ...
        col: ('DiscountAmountUsed', <class 'float'>, None, 24, 24, 0, True)
        col: ('SeatNumber', <class 'int'>, None, 10, 10, 0, True)
        col: ('OnHoldUntilTime', <class 'datetime.datetime'>, None, 19, 19, 0, True)
        col: ('GSTTaxable', <class 'bool'>, None, 1, 1, 0, False)
        col: ('ShortNote', <class 'str'>, None, 40, 40, 0, True)
        col: ('FoodStampsPayable', <class 'bool'>, None, 1, 1, 0, False)
        col: ('LiquorTaxApplied', <class 'bool'>, None, 1, 1, 0, False)
        col: ('PizzaLabelPrinted', <class 'bool'>, None, 1, 1, 0, False)
        col: ('EditTimestamp', <class 'datetime.datetime'>, None, 19, 19, 0, True)
        col: ('RemoteSiteNumber', <class 'int'>, None, 5, 5, 0, True)
        col: ('RemoteOrigRowID', <class 'int'>, None, 10, 10, 0, True)
        col: ('GlobalID', <class 'str'>, None, 30, 30, 0, True)
        col: ('RowVer', <class 'str'>, None, 30, 30, 0, True)
        col: ('SynchVer', <class 'datetime.datetime'>, None, 19, 19, 0, True)
        col: ('StoreNumber', <class 'int'>, None, 10, 10, 0, True)
        col: ('Kitchen1Printed', <class 'bool'>, None, 1, 1, 0, False)
        ...
        col: ('Kitchen6Printed', <class 'bool'>, None, 1, 1, 0, False)
        col: ('BarPrinted', <class 'bool'>, None, 1, 1, 0, False)
        col: ('CourseNumber', <class 'int'>, None, 10, 10, 0, True)
        col: ('ItemFired', <class 'bool'>, None, 1, 1, 0, False)
        col: ('HQRowID', <class 'str'>, None, 50, 50, 0, True)
        col: ('LastRowHash', <class 'str'>, None, 50, 50, 0, True)
        col: ('RowOwner', <class 'int'>, None, 5, 5, 0, True)
        col: ('RowGUID', <class 'str'>, None, 50, 50, 0, True)
    '''
    def insertOrderTransactions(self, orderId, orderItem):
        tableName = "OrderTransactions"
        cursor = self.conn.cursor()
        
        
        qmenu_item_id = util.getObjectField(orderItem["miInstance"], "id", defaultValue = '')
        sizeOptionIndex = util.getSizeOptionIndex(orderItem)
        qmenu_item_id = f"{qmenu_item_id}+{sizeOptionIndex}"
        menuItemID, menuName, printer = self.findMenuItemID(qmenu_item_id)
        if menuItemID == "":
            raise Exception(f"not found menuItemID for {qmenu_item_id}")


        orderTansaction = {
            "OrderID": orderId,
            "MenuItemID": menuItemID,
            "MenuItemUnitPrice": self.findMenuItemUnitPrice(orderItem),
            "Quantity": self.findQuantity(orderItem),
            "ExtendedPrice": self.findExtendedPrice(orderItem) * self.findQuantity(orderItem),
            "DiscountTaxable": True,      # disk: check,  for surcharge $2: uncheck
            "TransactionStatus": 1,
            "NotificationStatus": 1,
            "OnHoldUntilTime": datetime(9999,12,31),
            "GSTTaxable": 0,
            "FoodStampsPayable": 0,
            "LiquorTaxApplied": 0,
            "PizzaLabelPrinted": 0,
            "RemoteOrigRowID": 2,
            "GlobalID": 9,
            "RowVer": printer,
            "StoreNumber": 2,
            "Kitchen1Printed": 0,
            "Kitchen2Printed": 0,
            "Kitchen3Printed": 0,
            "Kitchen4Printed": 0,
            "Kitchen5Printed": 0,
            "Kitchen6Printed": 0,
            "BarPrinted": 0,
            "ItemFired": 0,
            "RowGUID": uuid.uuid4()
        }

        (insertStatement, valueList) = util.buildInsertStatement(tableName, orderTansaction)
        
        print(f"statement: {insertStatement}")
        print(f"values: {valueList}")
        cursor.execute(insertStatement, 
            valueList
        )

        self.conn.commit()

    
    def insertSurchargeInOrderTransactions(self, orderId):
        tableName = "OrderTransactions"
        cursor = self.conn.cursor()
        
        orderTansaction = {
            "OrderID": orderId,
            "MenuItemID": 377,
            "MenuItemUnitPrice": 2,
            "Quantity": 1,
            "ExtendedPrice": 2,
            "DiscountTaxable": False,      # disk: check,  for surcharge $2: uncheck
            "TransactionStatus": 1,
            "NotificationStatus": 1,
            "GSTTaxable": 0,
            "FoodStampsPayable": 0,
            "LiquorTaxApplied": 0,
            "PizzaLabelPrinted": 0,
            "RemoteOrigRowID": 2,
            "GlobalID": 9,
            "RowVer": "",
            "StoreNumber": 2,
            "Kitchen1Printed": 0,
            "Kitchen2Printed": 0,
            "Kitchen3Printed": 0,
            "Kitchen4Printed": 0,
            "Kitchen5Printed": 0,
            "Kitchen6Printed": 0,
            "BarPrinted": 0,
            "ItemFired": 0,
            "RowGUID": uuid.uuid4()
        }

        (insertStatement, valueList) = util.buildInsertStatement(tableName, orderTansaction)
        
        print(f"statement: {insertStatement}")
        print(f"values: {valueList}")
        cursor.execute(insertStatement, 
            valueList
        )

        self.conn.commit()


    def insertOrderHeaders(self, order) -> int:
        cursor = self.conn.cursor()
        rowUUID = uuid.uuid4()
        now = datetime.now()
        orderMap = {
            "OrderDateTime": now,
            "EmployeeID": 9,
            "StationID": 2,
            "OrderType": 3,
            "DeliveryCharge": 0,
            "DeliveryComp": 0,
            "SalesTaxRate": 7,
            "OrderStatus": 1,
            "AmountDue": util.getAmountDue(order),     # + tip
            "Subtotal": util.getOrderSubtotal(order),  # no tip, but + surcharge
            "CashGratuity": util.getTip(order),        # tip
            "SalesTaxAmountUsed": util.getTax(order),  # tax
            "GSTRate": 0,
            "GSTAmountUsed": 0,
            "SpecificCustomerName":  util.getSpecialCustomerName(order),  # <orderNumber>-<phone_last_4_digits>-<customer_name>
            "GuestCheckPrinted": True,  # checked
            "ServerBankAmount": 0,
            "Kitchen4AlreadyPrinted": 0,
            "Kitchen5AlreadyPrinted": 0,
            "Kitchen6AlreadyPrinted": 0,
            "LiquorTaxRate": 0,
            "LiquorTaxAmount": 0,
            "EditTimestamp": now,
            "RemoteOrigRowID": 0,
            "StoreNumber": 0,
            "BarTabPreAuth": 0,
            "RowGUID": rowUUID
        }

        (insertStatement, valueList) = util.buildInsertStatement("OrderHeaders", orderMap)
    
        print(f"statement: {insertStatement}")
        print(f"values: {valueList}")
        cursor.execute(insertStatement, 
            valueList
        )

        self.conn.commit()

        orderId = self.findOrderId(rowUUID)
        print(f"inserted an order with id: {orderId}")
        return orderId

    
    def findOrderId(self, rowUUID):
        cursor = self.conn.cursor()
        queryStatement = 'select * from OrderHeaders where RowGUID = ?'
        cursor.execute(queryStatement, rowUUID)
        row = cursor.fetchone()
        print(row)
        return row.OrderID
    

    def findMenuItemID(self, qmenu_item_id):
        if qmenu_item_id == '':
            print(f"no id for input orderItem: {qmenu_item_id}")
        
        try:
            (lasosichun_menu_id, lasichuan_menu_name, lasichuan_printer) = config.MENU_ITEM_MAP[qmenu_item_id]
        except:
            print(f"no corresponding Lao Sichuan menu item id found for {qmenu_item_id}, need to add it to the map!")
            (lasosichun_menu_id, lasichuan_menu_name, lasichuan_printer) = ("", "", "")

        return (lasosichun_menu_id, lasichuan_menu_name, lasichuan_printer)


    def findMenuItemUnitPrice(self, orderItem):
        return util.getOrderItemPrice(orderItem)
    
    def findQuantity(self, orderItem):
        return orderItem["quantity"]

    def findExtendedPrice(self, orderItem):
        return self.findMenuItemUnitPrice(orderItem)

'''
    # insert into "OrderHeaders"
    def insertOrderHeaders(self, order):
        cursor = self.conn.cursor()
        rowUUID = uuid.uuid4()
        insertStatement = """
            insert into OrderHeaders(
                OrderDateTime, 
                EmployeeID, 
                StationID, 
                OrderType, 
                SalesTaxRate, 
                OrderStatus, 
                AmountDue, 
                Subtotal, 
                SalesTaxAmountUsed, 
                RowGUID) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
    
        cursor.execute(insertStatement, 
            (
                datetime.now(),   # OrderDateTime
                100, # EmployeeID
                2,   # StationID
                3,   # OrderType
                7,   # SalesTaxRate
                2,   # OrderStatus
                util.getOrderSubtotal(order),  # AmountDue
                util.getOrderSubtotal(order),   # Subtotal
                0.0, # SalesTaxAmountUsed
                rowUUID # RowGUID
            )
        )

        self.conn.commit()

        orderId = self.findOrderId(rowUUID)
        print(f"inserted an order with id: {orderId}")
        return orderId
'''