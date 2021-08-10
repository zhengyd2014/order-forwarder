from order.orderRetriever import OrderRetriever
from order.config import DB_FILE, URL, TOKEN
import time
import sys
from order import util, accessImporter
import signal


stopped = False

def getCurrentTimeInString():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def stop(signal, frame):
    global stopped
    stopped = True
    print("\n got exit signal, stopping ...")

def main():
    global stopped
    print(f"{getCurrentTimeInString()}: start retrieving new orders ... ")

    retriever = OrderRetriever(URL, TOKEN)
    access = accessImporter.AccessImporter(DB_FILE)

    # Setup signal handler
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    while not stopped:
        print("sleep for 1 minutes")
        for sec in range(0, 60):
            if stopped:
                break

            print(f' {sec}', end='')
            sys.stdout.flush()
            time.sleep(1)
        print("")

        localTime = getCurrentTimeInString()
        newOrders = retriever.findNewOrders()

        lastOrderTime = retriever.lastOrderCreationTime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{localTime}: found {len(newOrders)} new orders.  (last order creation time: {lastOrderTime})")

        if len(newOrders) == 0:
            continue

        for order in newOrders:
            print("--------")
            util.printOrder(order, retriever.getMenuItems())
            print("")
            access.importOrder(order)

    access.close()
    print(f"{getCurrentTimeInString()}: stopped retrieving new orders and exit!")

if __name__=="__main__":
    main()