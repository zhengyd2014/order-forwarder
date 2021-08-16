
from datetime import datetime
import time


def getCurrentTimeInString():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def utcToLocal(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def getObjectField(order, fieldName, defaultValue = ''):
    return order.get(fieldName, defaultValue)


def getAmountDue(order):
	amountDue = getOrderSubtotal(order) + getTax(order)
	return round(amountDue, 2)


def getOrderSubtotal(order):
	subtotal = getAllDishesAmount(order) + getSurcharge(order)
	return round(subtotal, 2)


def getAllDishesAmount(order):
	amount = 0.0
	for orderItem in order["orderItems"]:
		item = getObjectField(orderItem, "miInstance", defaultValue = None)
		if item is None:
			continue

		
		price = getOrderItemPrice(orderItem)
		quantity = getObjectField(orderItem, "quantity", defaultValue = 1.0)
		amount += (price * quantity)
	
	return amount


def getOrderItemPrice(orderItem):
	item = getObjectField(orderItem, "miInstance", defaultValue = None)
	sizeOption = getSizeOption(orderItem)
	for op in sizeOption:
		if op["selected"]:
			return op["price"]
	
	raise Exception(f"can't find the price for the orderItem: {item['name']}")


def getSelectedSizeOption(orderItem):
	sizeOption = getSizeOption(orderItem)
	for index in range(0, len(sizeOption)):
		op = sizeOption[index]
		if op["selected"]:
			return op

	# no selected found, return the first one
	return sizeOption[0]


def getSizeOption(orderItem):
	item = getObjectField(orderItem, "miInstance", defaultValue = None)
	if item is None:
		raise Exception("not find miInstance in the orderItem")

	sizeOption = getObjectField(item, "sizeOptions", defaultValue = None)
	if sizeOption is None:
		raise Exception("no sizeOption for the orderItem")
	return sizeOption


# find the final qmenu id through orderItem
# the format is "qmenu_id+<index_of_size_option>"
def getQMenuItemId(orderItem, menu_items):

	# get selected sizeOption from order
	original_qmenu_item_id = getObjectField(orderItem["miInstance"], "id", defaultValue = '')
	selectedSizeOption = getSelectedSizeOption(orderItem)

	# find the corresponding sizeOption from menu by comparing the name
	menu_item = menu_items[original_qmenu_item_id]
	sizeOption = menu_item["sizeOptions"]
	sizeOptionIndex = 0
	for index in range(0, len(sizeOption)):
		op = sizeOption[index]
		if selectedSizeOption["name"] == op["name"]:
			sizeOptionIndex = index
			break

	# construct the final qmenu_item_id 
	qmenu_item_id = f"{original_qmenu_item_id}+{sizeOptionIndex}"
	return qmenu_item_id


def getSurcharge(order):
	surcharge = getObjectField(order, "surchargeAmount", defaultValue = 0.0)
	return surcharge

def getTip(order):
	tip = getObjectField(order, "tip", defaultValue = 0.0)
	return tip

def getTax(order):
	dishAmount = getAllDishesAmount(order)
	taxRate = getObjectField(order, "taxRate", defaultValue = 0.0)
	tax = round(taxRate * dishAmount, 2)
	return tax


# <orderNumber>-<phone_last_4_digits>-<customer_name>
def getSpecialCustomerName(order):
	orderNumber = getObjectField(order, "orderNumber", defaultValue = 0)
	customer = getObjectField(order, "customerObj", defaultValue = None)
	phoneNumber = getObjectField(customer, "phone", defaultValue = "")
	firstName = getObjectField(customer, "firstName", defaultValue = "")
	lastName = getObjectField(customer, "lastName", defaultValue = "")
	name = f"{orderNumber}-{phoneNumber[-4:]}-{firstName}.{lastName}"
	return name


def printOrder(order, menu_items):
	if order is None:
		print("order not found, try again!")
		return

	print(f"order number: {order['orderNumber']}")
	print(f"order Items: ")
	for orderItem in order["orderItems"]:
		item = orderItem["miInstance"]
		print(f"\tid: {getQMenuItemId(orderItem, menu_items)}, name: {item['name']}, price: {getOrderItemPrice(orderItem)}, quantity: {orderItem['quantity']}")
	print(f"tip: ${getTip(order)}")
	print(f"tax: ${getTax(order)}")
	print(f"subtotal: ${getOrderSubtotal(order)}")
	print(f"amountDue: ${getAmountDue(order)}")
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