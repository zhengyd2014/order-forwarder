import requests
import json
from order import util
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta

class OrderRetriever:
	def __init__(self, url, token):
		self.url = url
		self.token = token
		self.lastOrderCreationTime = self.getLastOrderCreationTime()

	def getAllOrders(self):
		headers = CaseInsensitiveDict()
		headers["Accept"] = "application/json"
		headers["Authorization"] = self.token

		resp = requests.get(self.url, headers=headers)

		if resp.status_code != 200:
			print(f"can't access website, check if token is assigned, or re-generate the token, exit!")
			print(f"error: status code: {resp.status_code}, error message: {resp.content}")
			exit(1)

		# load orders
		orders = json.loads(resp.content)
		newestOrderNumber = util.getObjectField(orders[0], "orderNumber", defaultValue = 0)
		oldestOrderNumber = util.getObjectField(orders[-1], "orderNumber", defaultValue = 0)
		print(f"> get {len(orders)} orders, oldest order number: {oldestOrderNumber}, newest order number: {newestOrderNumber}")
		return orders

	def getLastOrderCreationTime(self):
		orders = self.getAllOrders()
		maxCreationTime = datetime.now() - timedelta(minutes=5)
		for order in orders:
			creationTimeStr = util.getObjectField(order, "createdAt")
			creationTimeStr = creationTimeStr[0:creationTimeStr.index(".")]
			creationTime = datetime.strptime(creationTimeStr, '%Y-%m-%dT%H:%M:%S')
			maxCreationTime = max(maxCreationTime, creationTime)
		
		return maxCreationTime

	def findNewOrders(self):
		orders = self.getAllOrders()
		newOrders = []
		maxCreationTime = self.lastOrderCreationTime
		index = 0;
		for order in orders:
			orderId = util.getObjectField(order, "orderNumber", defaultValue = 0)
			creationTimeStr = util.getObjectField(order, "createdAt")
			creationTimeStr = creationTimeStr[0:creationTimeStr.index(".")]
			creationTime = datetime.strptime(creationTimeStr, '%Y-%m-%dT%H:%M:%S')
			# print(f">>>> comparing the {index} order: number: {orderId}, creation time: {creationTime}")
			if  creationTime > self.lastOrderCreationTime:
				print(f"> find new order with id {orderId}")
				newOrders.append(order)
				maxCreationTime = max(maxCreationTime, creationTime)
			index += 1
		
		self.lastOrderCreationTime = maxCreationTime
		return newOrders

	def getOrderByID(self, orderID):
		orders = self.getAllOrders()
		for order in orders:
			if orderID == util.getObjectField(order, "orderNumber", defaultValue = 0):
				return order

		return None





