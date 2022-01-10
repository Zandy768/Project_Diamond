import unittest, socket, ssl, urllib.request, json, hmac, pysftp

from app2Main import App2

class TestApp2(unittest.TestCase):

	def test_recieveTLSJSONPayload(self):
		failCondition = False
		try:
			App2.recieveTLSJSONPayload()

		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_logActivity(self):
		sampleMessage = "Hello World"
		try:
			App2.logActivity(sampleMessage)
			failCondition = False
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_encodePayloadHMAC(self):
		samplePayload = '{"Name": "Test"}'

		try:
			encodedPayload = App2.encodePayloadHMAC(samplePayload)
			failCondition = False
		except:
			failCondition = True

		self.assertFalse(failCondition)


	def test_hashPayload(self):
		samplePayload = '{"Name": "Test"}'
		sampleHex = 'd6c145a4c72462253f7b5bb1b1cbdeac97dec4e4ed8f8cc99983fc9875acb986'
		failCondition = False

		if hmac.compare_digest(App2.hashPayloadHMAC(samplePayload), sampleHex):
			failCondition = False
		else:
			failCondition = True
		self.assertFalse(failCondition)

	def test_sendSFTP(self):
		failCondition = False
		try:
			App2.sendSFTP('payloadFile.json', 'hash.txt')
			failConditon = False
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_createJSONFile(self):
		samplePayload = '{"Name": "Test"}'
		App2.createJSONFile('payloadTestFile.json', samplePayload)
		with open('payloadTestFile.json', 'r') as infile:
			inPayload = json.load(infile)
		self.assertIsNotNone(inPayload)

	def test_sendSFTP(self):
		failConditon = False
		try:
			App2.sendSFTP('payloadFile.json', 'hash.txt')
			failConditon = False
		except:
			failConditon = True
		self.assertFalse(failConditon)


if __name__ == '__main__':
	unittest.main()

