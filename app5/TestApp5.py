import unittest, socket, json, datetime, time
from pymongo import MongoClient

from app5Main import App5

class TestApp5 (unittest.TestCase):

	def test_recieveActivityLogs(self):
		failCondition = False
		try:
			sTime = time.time()
			while True:
				cTime = time.time()
				eTime = cTime - sTime
				if eTime > 4:
					break
				else:
					client = MongoClient('localhost', 27017)
					db = client.team6DB
					collections = db.logs
					App5.recieveActivityLogs(collections)
		except:
			failCondition = False
		self.assertFalse(failCondition)

	def test_sendActivityLogsToMongoDB(self):
		failCondition = False
		try:
			App5.sendActivityLogsToMongoDB()
		except:
			failCondition = True
		self.assertFalse(failCondition)

if __name__ == '__main__':
	unittest.main()

