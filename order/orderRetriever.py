import requests
import json
import util
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
		newOrders = [];
		maxCreationTime = self.lastOrderCreationTime
		for order in orders:
			creationTimeStr = util.getObjectField(order, "createdAt")
			creationTimeStr = creationTimeStr[0:creationTimeStr.index(".")]
			creationTime = datetime.strptime(creationTimeStr, '%Y-%m-%dT%H:%M:%S')
			# print(type(creationTime))
			# print(creationTime)


			if  creationTime > self.lastOrderCreationTime:
				newOrders.append(order)
				maxCreationTime = max(maxCreationTime, creationTime)
		
		self.lastOrderCreationTime = maxCreationTime
		return newOrders





