from order.orderRetriever import OrderRetriever
from order.config import DB_FILE, URL, TOKEN
import time
from order import util, accessImporter


def main():
    retriever = OrderRetriever(URL, TOKEN)
    access = accessImporter.AccessImporter(DB_FILE)

    orderID = int(input("input the order you want to find: "))
    
    order = retriever.getOrderByID(orderID)
    util.printOrder(order, retriever.getMenuItems())

    confirm = input("type 'y' to confirm import the order, other to abort: ").lower()
    if (confirm == "y"):
        access.importOrder(order)
    else:
        "aborted!"
    
    access.close()
    print("exit")

if __name__=="__main__":
    main()