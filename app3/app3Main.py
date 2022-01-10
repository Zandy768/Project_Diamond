"""
# Project: App3
# Purpose Details: To learn how how SFTP works as well as email
# Course: IST 411
# Author: Team 6
# Date Developed:10/22/20
# Last Date Changed:10/22/20
# Rev:1
"""

import json, smtplib, base64, pysftp, getpass, hmac, hashlib, Pyro4, socket, zlib
from email.mime.text import MIMEText

@Pyro4.expose
class App3:

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

	def emailPayload(email, payload):
		"""
		Sends email to designated email

		:param email: email address
		:param payload: payload to send
		:return: returns nothing
		"""
		msg = MIMEText(payload)
		msg['Subject'] = '411 project diamond'
		msg['From'] = email
		msg['To'] = email
		s = smtplib.SMTP_SSL('authsmtp.psu.edu', 465)
		s.sendmail(email, email, msg.as_string())

	def hashPayload(payload):
		"""
		hashes payload

		:param payload: payload to hash
		:return: hashed payload
		"""
		key = "This is a sample key"
		encodedKey = key.encode('utf-8')
		encodedPayload = payload.encode('utf-8')
		digesterSHA256 = hmac.new(encodedKey, encodedPayload, hashlib.sha256)
		hashPayload = digesterSHA256.hexdigest()
		return hashPayload

	def getFile(fileName):
		"""
		reads in file via SFTP

		:param fileName: name of file to read
		:return: read file contents
		"""
		readIn = open(fileName , 'r')
		holder = readIn.read()
		return holder

	def decodePayload(payload):
		"""
		decodes payload
		:param payload: payload to be decoded
		:return: decoded payload
		"""
		decodedPayload = base64.b64decode(payload)
		return decodedPayload

	def compareHash(hash1, hash2):
		"""
		compares if two signatures are the same

		:param hash1: the first signature
		:param hash2: the second signature
		:return: nothing
		"""
		print("comparing hashs")
		if hmac.compare_digest(hash1, hash2):
			print("The hashs are the same")
		else:
			print("The hashes are different")

	def compressPayload(payload):
		"""
		compresses the JSON payload

		:param payload: payload to be compressed
		:return: compressed payload
		"""
		payloadComp = zlib.compress(payload)
		checksum = zlib.crc32(payload)
		print("Checksum:", str(checksum))
		return payloadComp

	#Sends compressed payload via Pyro4
	def sendPayloadPyro(payloadComp):
		"""
		sends compressed payload via Pyro 4

		:param payloadComp: compressed payload to be send
		:return: nothing
		"""
		uri = input("Enter Pyro uri: ").strip()
		#app4 = Pyro4.Proxy("PYRONAME:app4")
		app4 = Pyro4.Proxy(uri)
		app4.receivePayload(payloadComp)

if __name__ == '__main__':
	try:
		with open('payloadFile.json', 'r') as infile:
                        payload = json.load(infile)
		print(payload)
		payloadHash = App3.hashPayload(payload)
		print(payloadHash)

		hash = App3.getFile('hash.txt')
		print(hash)
		App3.logActivity("App3 successfully got payload and hash from app2")

		App3.compareHash(payloadHash, hash)

		App3.emailPayload('akl5294@psu.edu', payload)
		App3.logActivity("App3 successfully emailed JSON Payload")

		bytePayload = bytes(payload, 'utf-8')
		print(bytePayload)
		payloadComp = App3.compressPayload(bytePayload)
		print(payloadComp)
		App3.logActivity("App3 successfully compressed JSON Payload")

		App3.sendPayloadPyro(payloadComp)
		App3.logActivity("App3 successfully sent JSON Payload to App 4 via Pyro")

	except Exception as e:
		print(e)
		failMsg = "App 3 has failed"
		App3.logActivity(failMsg)
