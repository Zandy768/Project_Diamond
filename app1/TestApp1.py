import unittest, socket, ssl, urllib.request, json

from app1Main import App1

class TestApp1(unittest.TestCase):

	def test_GetJSONPayload(self):
		samplePayload = App1.getJSONPayload('https://jsonplaceholder.typicode.com/posts/1/comments')
		self.assertIsNotNone(samplePayload)

	def test_SaveJSONPayload(self):
		samplePayload = App1.getJSONPayload('https://jsonplaceholder.typicode.com/posts/1/comments')
		App1.saveJSONPayload(samplePayload)
		with open('JSONPayload.json', 'r') as infile:
			inPayload = json.load(infile)
		self.assertIsNotNone(inPayload)

	def test_sendTLSJSONPayload(self):
		samplePayload = App1.getJSONPayload('https://jsonplaceholder.typicode.com/posts/1/comments')
		failCondition = False
		try:
			App1.sendTLSJSONPayload(samplePayload)
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_logActivity(self):
		sampleMessage = "Hello World"
		failCondition = False
		try:
			App1.logActivity(sampleMessage)
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_decryption(self):
		sampleCipherText = b'\xe7\xca$\xe0\xcdw\x91\xa3\xc3\xb9i\x8e\xae\x80\x86\xc5\xb6\x9a\xa6b\xff\xdb\x00\xa4}qV\x82#F\xc2M'
		payload = b'{"name":"andy", "userID" : 1}'
		if(App1.decryptPayloadAES(sampleCipherText) == payload):
			failCondition = False
		else:
			failCondition = True
		self.assertTrue(failCondition)


if __name__ == '__main__':
    unittest.main()
