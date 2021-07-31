
import unittest   # The test framework
from order import util, accessImporter
import json
from datetime import datetime
import time

orderObj2500 = json.loads('''
    {
  "_id": "60fd79f9b372b40008f110d6",
  "sendNotificationOnReady": true,
  "orderItems": [
    {
      "menuName": "Main Menu",
      "menuId": "1",
      "mcInstance": {
        "name": "Sichuan Style Appetizer",
        "description": "",
        "id": "1-2",
        "images": [],
        "collapsedIndexThreshold": 6
      },
      "miInstance": {
        "imageObjs": [],
        "cachedMinCost": -1,
        "cachedMaxCost": 6.25,
        "sizeOptions": [
          {
            "name": "regular",
            "price": 7.25,
            "selected": true
          }
        ],
        "name": "Sichuan Cold Noodles",
        "description": "",
        "price": 5.5,
        "sizes": [
          "$5.50"
        ],
        "id": "1-2-4",
        "category": "1-2",
        "inventory": null,
        "orderCount": 123,
        "translation": {
          "en": "Sichuan Cold Noodles"
        },
        "coverage": 0.730346621370561
      },
      "mcSelectedMenuOptions": [],
      "miSelectedMenuOptions": [],
      "quantity": 1,
      "specialInstructions": null,
      "id": "1627224201926"
    },
    {
      "menuName": "Main Menu",
      "menuId": "1",
      "mcInstance": {
        "name": "Fried Rice & Noodles",
        "description": "",
        "id": "1-5",
        "images": [],
        "collapsedIndexThreshold": 14
      },
      "miInstance": {
        "imageObjs": [],
        "cachedMinCost": -1,
        "cachedMaxCost": -1,
        "sizeOptions": [
          {
            "name": "Pork",
            "price": 15.95,
            "selected": false
          },
          {
            "name": "Chicken",
            "price": 15.95,
            "selected": false
          },
          {
            "name": "Vegetables",
            "price": 15.95,
            "selected": true
          }
        ],
        "name": "Pan Fried Noodles (Pork, Chicken, Beef or Vegetables)",
        "description": "",
        "price": 11.95,
        "sizes": [
          "Pork ($11.95)",
          "Chicken ($11.95)",
          "Beef ($11.95)",
          "Vegetables ($11.95)"
        ],
        "id": "1-5-8",
        "category": "1-5",
        "inventory": null,
        "translation": {
          "en": "Pan Fried Noodles (Pork, Chicken, Beef or Vegetables)"
        },
        "orderCount": 76,
        "coverage": 0.8394288444184935
      },
      "mcSelectedMenuOptions": [],
      "miSelectedMenuOptions": [],
      "quantity": 1,
      "specialInstructions": null,
      "id": "1627224244576"
    },
    {
      "menuName": "Main Menu",
      "menuId": "1",
      "mcInstance": {
        "name": "Fried Rice & Noodles",
        "description": "",
        "id": "1-5",
        "images": [],
        "collapsedIndexThreshold": 14
      },
      "miInstance": {
        "imageObjs": [],
        "cachedMinCost": -1,
        "cachedMaxCost": -1,
        "sizeOptions": [
          {
            "name": "Chicken",
            "price": 11.75,
            "selected": false
          },
          {
            "name": "Roast Pork",
            "price": 11.75,
            "selected": false
          },
          {
            "name": "Vegetable",
            "price": 11.75,
            "selected": true
          }
        ],
        "name": "Rice Noodle (Pork, Chicken or Vegetable)",
        "description": "",
        "price": 8.25,
        "sizes": [
          "Chicken ($8.25)",
          "Roast Pork ($8.25)",
          "Vegetable ($8.25)"
        ],
        "id": "1613846336276",
        "category": "1-5",
        "inventory": null,
        "orderCount": 50,
        "translation": {
          "en": "Rice Noodle (Pork, Chicken or Vegetable)"
        },
        "coverage": 0.8954827750942195
      },
      "mcSelectedMenuOptions": [],
      "miSelectedMenuOptions": [],
      "quantity": 1,
      "specialInstructions": null,
      "id": "1627224255572"
    },
    {
      "menuName": "Main Menu",
      "menuId": "1",
      "mcInstance": {
        "name": "Seasonal Green Vegetables",
        "description": "",
        "id": "1-16",
        "images": [],
        "collapsedIndexThreshold": 3
      },
      "miInstance": {
        "imageObjs": [],
        "cachedMinCost": -1,
        "cachedMaxCost": 13.95,
        "sizeOptions": [
          {
            "name": "Seasonal Green Vegetables",
            "price": 14.95,
            "selected": true
          }
        ],
        "name": "Stir Fried Cauliflower",
        "description": "",
        "price": 9.95,
        "sizes": [
          "Seasonal Green Vegetables ($9.95)"
        ],
        "id": "1524941155338",
        "category": "1-16",
        "inventory": null,
        "disabled": false,
        "orderCount": 57,
        "translation": {
          "en": "Stir Fried Cauliflower"
        },
        "coverage": 0.8814692924252879
      },
      "mcSelectedMenuOptions": [],
      "miSelectedMenuOptions": [],
      "quantity": 1,
      "specialInstructions": null,
      "id": "1627224359743"
    }
  ],
  "surchargeName": "Order Service Fee",
  "surchargeAmount": 2,
  "ccProcessingRate": null,
  "taxRate": 0.07,
  "tip": 4.99,
  "timeToDeliver": "2021-07-25T17:30:00.000Z",
  "specialInstructions": "No meat , no seafood, or no eggs, or no meat sauce or seafood sauce",
  "type": "PICKUP",
  "deliveryCharge": 0,
  "fees": [],
  "paymentObj": {
    "paymentType": "CREDITCARD",
    "method": "IN_PERSON"
  },
  "customerObj": {
    "_id": "60b337c01a43f00008fc94c0",
    "email": "fredzheng@gmail.com",
    "firstName": "Fred",
    "lastName": "Zheng",
    "phone": "555-555-5555"
  },
  "deliveryDistance": null,
  "orderNumber": 2500,
  "customerPreviousOrderStatus": {
    "order": "60b39fa2a4cb2f0009bbd80a",
    "status": "COMPLETED",
    "createdAt": "2021-05-30T16:40:23.721Z",
    "updatedBy": "BY_RESTAURANT"
  },
  "createdAt": "2021-07-25T14:49:29.219Z",
  "statuses": [
    {
      "status": "SUBMITTED",
      "createdAt": "2021-07-25T14:49:29.219Z"
    },
    {
      "status": "CONFIRMED",
      "createdAt": "2021-07-25T14:52:52.043Z"
    }
  ],
  "timeToDeliverEstimate": "2021-07-25T17:30:00.000Z"
}
    ''')

orderObj1 = json.loads('''
{
  "orderItems": [
    {
      "miInstance": {
        "name": "Sichuan Cold Noodles",
        "price": 5.0
      },
      "quantity": 5,
      "id": "1627224201926"
    },
    {
      "miInstance": {
        "name": "Pan Fried Noodles (Pork, Chicken, Beef or Vegetables)",
        "price": 25.0
      },
      "quantity": 3,
      "id": "1627224244576"
    }
  ],
  "surchargeName": "Order Service Fee",
  "surchargeAmount": 2,
  "taxRate": 0.07,
  "tip": 1.0,
  "orderNumber": 2500
}
''')


class Test_Util(unittest.TestCase):
    def test_createdAt(self):
        creationTimeStr = util.getObjectField(orderObj2500, "createdAt")   # 2021-07-25T14:52:52.043Z 
        creationTimeStr = creationTimeStr[0:creationTimeStr.index(".")]    # 2021-07-25T14:49:29

        creationTime = datetime.strptime(creationTimeStr, '%Y-%m-%dT%H:%M:%S')
        creationTime = util.utcToLocal(creationTime)
        localCreationTimeStr = creationTime.strftime("%Y-%m-%d %H:%M:%S")  # 2021-07-25 10:49:29

        self.assertEqual(localCreationTimeStr, "2021-07-25 10:49:29")

    def test_getSubtotal(self):
        subtotal = util.getOrderSubtotal(orderObj1)

        #  dish price = 5.0 * 5 + 25.0 * 3 = 100
        #  tax = 100 * 0.07 = 7
        #  surcharge = 2
        #  tip = 1

        #  subtotal = dish price + surcharge
        #  tax = dish_price * taxRate
        #  amountDue = subtotal + tax + tip
        self.assertEqual(subtotal, 102.0)
        self.assertEqual(util.getAmountDue(orderObj1), 110.0)


    # def test_db(self):
    #   print("print db information")
    #   access = accessImporter.AccessImporter("Z:\\new-01-16.mdb")
    #   print(f"---- tables ----")
    #   access.printAllTables()

    #   print("---- table OrderHeaders ----")
    #   access.describeTable("OrderHeaders")

    #   print("---- table OrderTransactions ----")
    #   access.describeTable("OrderTransactions")

    #   print("---- table MenuItems ----")
    #   access.describeTable("MenuItems")

    #   access.displayMenuItems()
    #   print("end of test_db")


    # def test_insertOrderHeaders(self):
    #   access = accessImporter.AccessImporter("Z:\\new-01-16.mdb")
    #   orderId = access.insertOrderHeaders(orderObj2500)
    #   print(f"orderId: {orderId}")

    def test_insertOrderTransactions(self):
      access = accessImporter.AccessImporter("Y:\\new-01-16.mdb")
      orderId = 1962
      orderItem = orderObj2500["orderItems"][0]
      access.insertOrderTransactions(orderId, orderItem)


    def test_findMenuItemID(self):
      access = accessImporter.AccessImporter("Y:\\new-01-16.mdb")

      # find existed id
      qmenu_item_id = orderObj1["orderItems"][0]["id"]
      print(f"qmenu_item_id: {qmenu_item_id}")
      lsc_menu_id = access.findMenuItemID(qmenu_item_id)
      self.assertEqual(lsc_menu_id, "66")


      # find no-existed id
      qmenu_item_id = "not_existed_id"
      self.assertRaises(Exception, access.findMenuItemID(qmenu_item_id))

    
    def test_buildStatement(self):
      mapObject = {"orderID" : "123", "time" : "2021-07-30", "other" : "value"}
      access = accessImporter.AccessImporter("Y:\\new-01-16.mdb")
      (statement, valueList) = util.buildInsertStatement("OrderTransactions", mapObject)
      self.assertEqual(statement, "insert into OrderTransactions (orderID,time,other) values (?,?,?)")
      print(f"statement: {statement}")
      print(f"values: {valueList}")
    
      

if __name__ == '__main__':
    unittest.main()

