import unittest, zlib, Pyro4, serpent
from app4Main import App4

class TestApp4 (unittest.TestCase):

	def test_receivePayload(self):
		uri = input("Enter Pyro uri: ").strip()
		app4 = Pyro4.Proxy(uri)
		try:
			payload = '{"name":"andy", "userID" : 1}'
			print("okay")
			compressedPayload = zlib.compress(payload.encode('utf-8'))
			print("okay too")
			app4.receivePayload(compressedPayload)
			failCondition = False
		except:
			failCondition = True
		self.assertFalse(failCondition)


	def test_decompressPayload(self):
		payload = '{"name":"andy", "userID" : 1}'
		compressedPayload = zlib.compress(payload.encode('utf-8'))
		try:
			App4.decompressPayload(compressedPayload)
			failCondition = False
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_encryption(self):
		payload = b'{"name":"andy", "userID" : 1}'

		try:
			App4.encryptPayloadAES(payload)
			failCondition = False
		except:
			failCondition = True

if __name__ == '__main__':
	unittest.main()

