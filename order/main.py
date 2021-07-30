from order.orderRetriever import OrderRetriever
from order.config import URL, TOKEN
import time
from order import util, accessImporter


def main():
    retriever = OrderRetriever(URL, TOKEN)
    access = accessImporter.AccessImporter("Y:\\new-01-16.mdb")

    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{startTime}: start retrieving new orders ... ")

    while True:
        print("sleep for 1 minutes")
        time.sleep(60)

        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        newOrders = retriever.findNewOrders()

        lastOrderTime = retriever.lastOrderCreationTime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{localTime}: found {len(newOrders)} new orders.  (last order creation time: {lastOrderTime})")

        if len(newOrders) == 0:
            continue

        
        for order in newOrders:
            print("--------")
            util.printOrder(order)
            print("")
            access.importOrder(order)
            
    # stopTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(f"{stopTime}: stopped retrieving new orders.")

if __name__=="__main__":
    main()