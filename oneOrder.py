from order.orderRetriever import OrderRetriever
from order.config import DB_FILE, URL, TOKEN
import time
from order import util, accessImporter
import logging
import sys

log_file = open(f"{util.getCurrentTimeAsFileName('main')}", mode="w", encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    retriever = OrderRetriever(URL, TOKEN)
    access = accessImporter.AccessImporter(DB_FILE, retriever.menu_items)

    orderID = int(input("input the order you want to find: "))
    
    order = retriever.getOrderByID(orderID)
    util.printOrder(order, retriever.getMenuItems())

    confirm = input("type 'y' to confirm import the order, other to abort: ").lower()
    if (confirm == "y"):
        access.importOrder(order)
    else:
        "aborted!"
    
    print("exit")

if __name__=="__main__":
    main()