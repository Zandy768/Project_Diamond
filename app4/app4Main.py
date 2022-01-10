"""
# Project: App4
# Purpose Details:
# Course: IST 411
# Author: Team 6
# Date Developed:11/11/20
# Last Date Changed:11/11/20
# Rev:1
"""

import json, Pyro4, serpent, zlib, pika, socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

@Pyro4.expose
class App4():

	def receivePayload(self, payloadComp):
		"""
		Recieves payload from App3 and activates the decompression method
		"""
		if Pyro4.config.SERIALIZER == "serpent" and type(payloadComp) is dict:
			payloadComp = serpent.tobytes(payloadComp)
		print(payloadComp)
		App4.logActivity("App 4 successfully recieved compressed JSON Payload")
		App4.decompressPayload(payloadComp)

	def decompressPayload(payload):
		"""
		decompresses the payload and then ecrypts it via AES and sends it to App1

		:param payload: payload to be decompressed
		:return: nothing
		"""
		payloadDeComp = zlib.decompress(payload)
		print(payloadDeComp.decode('utf-8'))
		App4.logActivity("App 4 successfully decompressed JSON Payload")
		print()
		App4.encryptPayloadAES(payloadDeComp)

	def encryptPayloadAES(payload):
		"""
		Encrypts a payload via AES and sends it to App1

		:param payload: payload to be encrypted
		:return: nothing
		"""
		key = b'2646294A404E635266556A586E327233'
		IV = b'0123456789abcdef'
		mode = AES.MODE_CBC

		paddedPayload = pad(payload, 16)
		print("Padded Payload:", paddedPayload)

		encryptor = AES.new(key, mode, IV=IV)
		ciphertext = encryptor.encrypt(paddedPayload)
		print()
		print("Ciphertext:", ciphertext)
		App4.logActivity("App 4 successfully encrypted JSON Payload")

		App4.sendPayloadRabbitMQ(ciphertext)

	def sendPayloadRabbitMQ(payload):
		"""
		Sends an encrypted payload to App1

		:param payload: payload to be sent
		:return: nothing
		"""
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		channel.queue_declare(queue='Team6')
		channel.basic_publish(exchange='',routing_key='Team6',body = payload)
		channel.close()
		connection.close()
		App4.logActivity("App 4 successfully sent JSON Payload to App1 via RabbitMQ")

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
		daemon = Pyro4.Daemon()
		uri = daemon.register(App4)
		#newApp4 = Pyro4.locateNS()
		print("Object uri =", uri)
		#newApp4.register("app4", uri)

		daemon.requestLoop()

	except Exception as e:
		print(e)
