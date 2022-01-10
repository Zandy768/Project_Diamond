"""
# Project: Logging to MongoDB
# Purpose Details: To log all actions to a db
# Course: IST 411
# Author: Andy Liu
# Date Developed: 10/9/20
# Last Date Changed:10/9/20
# Rev:1
"""

import sys, socket, json, datetime
from pymongo import MongoClient
from eve import Eve
#settings = {'DOMAIN': {'logmessage': {}}}
app = Eve(settings='settings.py')

class App5:

	def recieveActivityLogs(collections):
		"""
		recieves activity logs from other apps
		:param collections:
		:return: nothing
		"""
		logServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		logServer.bind(('localhost', 9999))
		logServer.listen(5)
		while True:
			(clientsocket, address) = logServer.accept()
			message = clientsocket.recv(1024).decode()
			deMessage = str(message)
			print(deMessage)
			time = str(datetime.datetime.now())
			collections.insert({"time": time , "message": deMessage})

	def sendActivityLogsToMongoDB():
		"""
		sends activity logs to MongoDB
		:return: The collection being used
		"""
		client = MongoClient('localhost', 27017)
		db = client.team6DB
		collections = db.logs
		return collections


if __name__ == '__main__':
	try:
		collections = App5.sendActivityLogsToMongoDB()
		App5.recieveActivityLogs(collections)
		app.run()

	except Exception as e:
		print(e)
