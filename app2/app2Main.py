"""
Project: App2
Purpose Details: To learn how clients connect to servers using networking
Course: IST 411
Author: Team 6
Date Developed:9/26/20
Last Date Changed:10/15/20
Rev:2
"""

import socket, json, ssl, base64, hashlib, hmac, getpass, pysftp

class App2:

	def recieveTLSJSONPayload():
		"""
		Receives JSON payload from App1 via TLS.

		:return: Returns nothing
		"""

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket = ssl.wrap_socket(s,
			server_side=True,
			certfile="server.crt",
			keyfile="server.key")
		serversocket.bind(('localhost', 1111))
		serversocket.listen(5)
		while True:
			print("waiting on connection")
			(clientsocket, address) = serversocket.accept()
			payload = clientsocket.recv(1024).decode('utf-8')
			with open('sample.json' , 'w') as outFile:
				jsonObj = outFile.write(json.dumps(payload))
			break

	def encodePayloadHMAC(payload):
		"""
		Encodes the Payload with HMAC.

		:param payload: JSON Payload receieved from App1
		:return: Returns payload encoded in HMAC
		"""

		encodedPayload = base64.b64encode(bytes(payload, 'utf-8'))
		return encodedPayload

	def hashPayloadHMAC(payload):
		"""
		Hashes HMAC payload.

		:param payload: HMAC payload
		:return: returns hashed payload
		"""

		key = "This is a sample key"
		encodedKey = key.encode('utf-8')
		encodedPayload = payload.encode('utf-8')
		digesterPayload = hmac.new(encodedKey, encodedPayload, hashlib.sha256)
		digestPayload = digesterPayload.hexdigest()

		return digestPayload

	def sendSFTP(payload, hash):
		"""
		Sends file to app3 via SFTP.

		:param payload: Hashed payload
		:param hash: Hash
		:return: Returns nothing
		"""

		p = getpass.getpass()
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		cinfo = {'cnopts':cnopts, 'host':'oz-ist-lvmjxo.oz.psu.edu', 'username':'akl5294', 'password':p, 'port':1855}
		with pysftp.Connection(**cinfo) as sftp:
			sftp.put(payload , 'abist411fa20Team6/app3/payloadFile.json')
			sftp.put(hash, 'abist411fa20Team6/app3/hash.txt')

	def createJSONFile(fileName, payload):
		"""
		Creates JSON file.

		:param fileName: Name of JSON file
		:param payload: JSON Payload
		:return: Returns nothing
		"""

		with open(fileName, 'w') as outfile:
			print(payload)
			outfile.write(json.dumps(payload))

	def createHashFile(fileName, payload):
		"""
		Creates hash file.

		:param fileName: Name of hash file
		:param payload: Hashed payload
		:return: Returns nothing
		"""

		with open(fileName, 'w') as outfile:
			payload = payload.decode('utf-8')
			outfile.write(payload)

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
		App2.recieveTLSJSONPayload()
		with open('sample.json', 'r') as infile:
			inPayload = json.load(infile)
		App2.logActivity("App 2 successfully recieved and printed JSON Payload from App1")
		print("Recieved Payload")
		App2.createJSONFile('payloadFile.json', inPayload)
		print("Payload Saved")

		print("Payload Hashed")
		hashedPayload = App2.hashPayloadHMAC(inPayload)
		App2.createHashFile('hash.txt', hashedPayload.encode('utf-8'))
		App2.logActivity("App 2 successfully hashed Payload")

		App2.sendSFTP('payloadFile.json', 'hash.txt')
		App2.logActivity("App 2 successfully sent JSON Payload to App3 via SFTP")

	except Exception as e:
		print(e)
		failMsg = "App 2 has failed to recieve and/or send JSON Payload"
		App2.logActivity(failMsg)

