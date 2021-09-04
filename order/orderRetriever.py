import requests
import json
from order import util
from requests.structures import CaseInsensitiveDict
from datetime import datetime, timedelta
import logging
import sys
import time


class OrderRetriever:
	def __init__(self, url, token):
		self.request_count = 0
		self.url = url
		self.token = token
		self.lastOrderCreationTime = self.getLastOrderCreationTime()
		self.menu_items = self.getAllMenus()


	def getMenuItems(self):
		return self.menu_items


	def get(self, url):
		headers = CaseInsensitiveDict()
		headers["Accept"] = "application/json"
		headers["Authorization"] = self.token

		# retry
		retries = 1
		success = False
		while not success:
			try:
				resp = requests.get(url, headers=headers)
				self.request_count += 1
				success = True
			except Exception as e:
				wait = retries * 10
				if wait < 60:
					logging.error('sucessfully sent {self.request_count} requests, then starting fail. Waiting %s secs and re-trying...' % wait)
				else:
					logging.error(f"retried {retries} times, still fail exit!")
					raise e
				sys.stdout.flush()
				time.sleep(wait)
				retries += 1

		if resp.status_code != 200:
			logging.error(f"can't access website, check if token is assigned, or re-generate the token, exit!")
			logging.error(f"error: status code: {resp.status_code}, error message: {resp.content}")
			exit(1)
		
		return resp

	def getAllOrders(self):
		resp = self.get(self.url)

		# load orders
		orders = json.loads(resp.content)
		resp.close()
		newestOrderNumber = util.getObjectField(orders[0], "orderNumber", defaultValue = 0)
		oldestOrderNumber = util.getObjectField(orders[-1], "orderNumber", defaultValue = 0)
		logging.info(f"> get {len(orders)} orders, oldest order number: {oldestOrderNumber}, newest order number: {newestOrderNumber}")
		return orders
	

	def getAllMenus(self):
		## hardcoded menu url here, as I don't want to modify config file
		menu_url = "https://9v8upsmsai.execute-api.us-east-1.amazonaws.com/prod/biz/restaurant"
		resp = self.get(menu_url)
		menus = json.loads(resp.content)["menus"]
		menu_items = {}

		'''
		menus: {
			0: {
				mcs: {
					0: {
						mis: {
							0: {
								id: "1-1-1",
								sizeOptions: {
									0: {
										name: "regular",
										price: 5.5
									}
								}
							}
						}
					}
				}
			}
		} 
		'''
		for menu_category in menus:
			mcs = menu_category["mcs"]
			for menu_subcategory in mcs:
				mis = menu_subcategory["mis"]
				for menu_item in mis:
					menu_items[menu_item["id"]] = menu_item

		return menu_items


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
				logging.info(f"> find new order with id {orderId}")
				newOrders.insert(0, order)
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





