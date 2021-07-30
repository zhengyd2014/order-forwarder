
from datetime import datetime
import time

def utcToLocal(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def getObjectField(order, fieldName, defaultValue = ''):
    return order.get(fieldName, defaultValue)

def getOrderSubtotal(order):
	subtotal = 0.0
	for orderItem in order["orderItems"]:
		item = getObjectField(orderItem, "miInstance", defaultValue = None)
		if item is None:
			continue

		price = getObjectField(item, "price", defaultValue = 0.0)
		quantity = getObjectField(orderItem, "quantity", defaultValue = 1.0)
		subtotal += (price * quantity)

	taxRate = getObjectField(order, "taxRate", defaultValue = 0.0)
	subtotal += (taxRate * subtotal)

	surcharge = getObjectField(order, "surchargeAmount", defaultValue = 0.0)
	tip = getObjectField(order, "tip", defaultValue = 0.0)
	subtotal += (surcharge + tip)

	subtotal = round(subtotal, 2)

	return subtotal


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
	print(f"createdAt(UTC): {order['createdAt']}")

	# customer
	customer = order["customerObj"]
	print(f"customer: email: {customer.get('email', '')}, name: {customer.get('firstName','')} {customer.get('lastName','')}, phone: {customer.get('phone','')}")


def buildInsertStatement(tableName, mapObj):
	nameList = []
	valueList = []
	questionMarks = []
	for key, value in mapObj.items():
		nameList.append(key)
		questionMarks.append("?")
		valueList.append(value)
	
	statement = f'insert into {tableName} ({",".join(nameList)}) values ({",".join(questionMarks)})'
	return (statement, valueList)