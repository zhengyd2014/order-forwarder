import pyodbc
from datetime import datetime
import uuid
 
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=/Users/fzheng/Downloads/new-01-16.mdb;')
cursor = conn.cursor()
 
   
#for row in cursor.fetchall():
#   print (row)
 
tableName = "OrderHeaders"
 
cursor.execute(f'select * from "{tableName}"')
for col in cursor.description:
    print(f'\tcol: {col}')
 
now = datetime.now()
#format = "%d/%m/%Y %H:%M:%S"
#time1 = now.strftime(format)
 
myUUID = uuid.uuid4()
insert = f"insert into OrderHeaders(OrderDateTime, EmployeeID, StationID, OrderType, SalesTaxRate, OrderStatus, AmountDue, Subtotal, SalesTaxAmountUsed, RowGUID) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
cursor.execute(insert, (now, 10, 2, 3, 7, 2, 5.5, 5.5, 0.5, myUUID))
conn.commit()