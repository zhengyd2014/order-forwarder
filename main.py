from order.orderRetriever import OrderRetriever
from order.config import DB_FILE, URL, TOKEN
import time
import sys
from order import util, accessImporter
from order.util import getCurrentTimeInString
import signal
import traceback

## init logging ##
import logging
log_file = f"{getCurrentTimeInString()}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(r"{}".format(log_file), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)



stopped = False

def stop(signal, frame):
    global stopped
    stopped = True
    logging.info("\n got exit signal, stopping ...")

def main():
    global stopped
    logging.info(f"{getCurrentTimeInString()}: start retrieving new orders ... ")

    retriever = OrderRetriever(URL, TOKEN)
    access = accessImporter.AccessImporter(DB_FILE, retriever.menu_items)

    # Setup signal handler
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    while not stopped:
        logging.info("sleep for 1 minutes")
        for sec in range(0, 60):
            if stopped:
                break

            print(f' {sec}', end='')
            sys.stdout.flush()
            time.sleep(1)
        print("")

        try:
            localTime = getCurrentTimeInString()
            newOrders = retriever.findNewOrders()

            lastOrderTime = retriever.lastOrderCreationTime.strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"{localTime}: found {len(newOrders)} new orders.  (last order creation time: {lastOrderTime})")

            if len(newOrders) == 0:
                continue
        
            for order in newOrders:
                print("--------")
                util.printOrder(order, retriever.getMenuItems())
                print("")
                access.importOrder(order)
        except:
            traceback_info = traceback.format_exc()
            logging.error(traceback_info)
            with open(f"exception-{getCurrentTimeInString()}.txt", "w") as excpetion_file:
                excpetion_file.write(traceback_info)
            stopped = True
            break

    # access.close()
    logging.info(f"{getCurrentTimeInString()}: stopped retrieving new orders and exit!")

if __name__=="__main__":
    main()