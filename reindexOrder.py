from order.config import DB_FILE
from order import util, dbReindex
import logging
import sys

log_file = open(f"{util.getCurrentTimeAsFileName('reindexOrder')}", mode="w", encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    dbIndexer = dbReindex.DbReindexer(DB_FILE)
    dbIndexer.reindex()
    
    print("reindex finished")

if __name__=="__main__":
    main()