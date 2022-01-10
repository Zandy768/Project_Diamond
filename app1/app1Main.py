"""
Project: app1
Purpose Details: To learn how to get a url and use clients connect to servers using networking
Course: IST 411
Author: Team 6
Date Developed:9/25/20
Last Date Changed:10/15/20
Rev:4
"""

import socket, ssl, urllib.request, json, pika, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class App1:
	"""
	This is the first application
	"""

	def getJSONPayload(link):
		"""
		Gets JSON payload from URL.

		:param link:Payload link
		:return: Returns retrieved payload
		"""

		response = urllib.request.urlopen(link)
		payload = response.read()
		return payload

	def saveJSONPayload(payload):
		"""
		Saves JSON payload as a file.

		:param payload: The retrieved payload
		:return: returns nothing
		"""

		decodedPayload = json.loads(payload.decode('utf-8'))
		print(decodedPayload)
		with open('JSONPayload.json', 'w') as outFile:
			jsonObjPayload = outFile.write(json.dumps(decodedPayload))

	def sendTLSJSONPayload(payload):
		"""
		Sends activity/log to app5

		:param payload: json payload to send to App2
		:return: Returns nothing
		"""

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssl_sock = ssl.wrap_socket(s,
			certfile="server.crt",
			keyfile="server.key")
		ssl_sock.connect(('localhost',1111))
		ssl_sock.send(payload)
		ssl_sock.close()

	def getMQpayload():
		"""
		Gets RabbitMQ payload from app4.

		:return: returns nothing
		"""

		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='Team6')
		def callback(ch, method, properties, body):
			print(body)
			App1.logActivity("App 1 successfully received encrypted JSON Payload from App4")
			App1.decryptPayloadAES(body)
			App1.logActivity("App 1 successfully decrypted JSON Payload")
			channel.stop_consuming()
		channel.basic_consume('Team6',callback, auto_ack=True)
		channel.start_consuming()

		channel.close()
		connection.close()

	def decryptPayloadAES(payload):
		"""
		Decryptes encrypted Payload from app4.

		:param payload: Encrypted payload from app4
		:return: Returns nothing
		"""


		key = b'2646294A404E635266556A586E327233'
		IV = b'0123456789abcdef'
		mode = AES.MODE_CBC

		decryptor = AES.new(key, mode, IV=IV)
		ciphertext = decryptor.decrypt(payload)

		payload = unpad(ciphertext, 16)
		print()
		print("Decrypted Payload:", payload)

	def logActivity(message):
		"""
		Sends activity/log to app5

		:param message: Success/Failed message to app5
		:return: Returns nothing
		"""

		s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s2.connect(('localhost', 9999))
		byteMsg = bytes(message, 'utf-8')
		s2.send(byteMsg)
		s2.close()

if __name__ == '__main__':
	try:
		startTime = time.perf_counter()
		print("Start Time:", startTime)
		print()
		url = 'https://jsonplaceholder.typicode.com/posts/1/comments'
		payload = App1.getJSONPayload(url)
		App1.logActivity("App 1 successfully got JSON Payload")
		App1.saveJSONPayload(payload)
		App1.logActivity("App 1 successfully saved JSON Payload")
		App1.sendTLSJSONPayload(payload)
		successMsg = "App 1 successfully sent JSON Payload"
		App1.logActivity(successMsg)
		App1.getMQpayload()
		endTime = time.perf_counter()
		totalTime = endTime - startTime
		print()
		print("Total Time:", totalTime, "seconds")

	except Exception as e:
		print(e)
		failMsg = "App 1 failed to send JSON Payload"
		App1.logActivity(failMsg)

