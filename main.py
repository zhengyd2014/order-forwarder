from orderRetriever import OrderRetriever
from config import URL, TOKEN
import time


def printOrder(order):
	if order is None:
		print("order not found, try again!")
		return

	print(f"order number: {order['orderNumber']}")
	print(f"order Items: ")
	for orderItem in order["orderItems"]:
		item = orderItem["miInstance"]
		print(f"\tid: {item['id']}, name: {item['name']}, price: ${item['price']}, quantity: {orderItem['quantity']}")
	print(f"tip: ${order['tip']}")
	print(f"type: {order['type']}")
	print(f"createdAt: {order['createdAt']}")

	# customer
	customer = order["customerObj"]
	print(f"customer: email: {customer['email']}, name: {customer['firstName']} {customer['lastName']}, phone: {customer['phone']}")


def main():
    retriever = OrderRetriever(URL, TOKEN)
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{startTime}: start retrieving new orders ... ")

    while True:
        print("sleep for 1 minutes")
        time.sleep(60)

        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        newOrders = retriever.findNewOrders()

        lastOrderTime = retriever.lastOrderCreationTime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{localTime}: found {len(newOrders)} new orders.  (last order creation time: {lastOrderTime})")

        for order in newOrders:
            print("--------")
            printOrder(order)
            print("")
        
    # stopTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(f"{stopTime}: stopped retrieving new orders.")

if __name__=="__main__":
    main()