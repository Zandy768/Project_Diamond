import unittest, json, smtplib, base64, pysftp, getpass, hmac
from email.mime.text import MIMEText

from app3Main import App3

class TestApp3(unittest.TestCase):

	def test_logActivity(self):
		sampleMessage = "Hello World"
		failCondition = False
		try:
			App3.logActivity(sampleMessage)
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_emailPayload(self):
		sampleJSON = '{"Name": "Test"}'
		samplePayload = App3.hashPayload(sampleJSON)
		failCondition = False
		try:
			App3.emailPayload('akl5294@pau.edu', samplePayload)
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_hashPayload(self):
		samplePayload = '{"Name": "Test"}'
		sampleHex = 'd6c145a4c72462253f7b5bb1b1cbdeac97dec4e4ed8f8cc99983fc9875acb986'

		if hmac.compare_digest(App3.hashPayload(samplePayload), sampleHex):
			failCondition = False
		else:
			failCondition = True
		self.assertFalse(failCondition)

	def test_getFile(self):
		file = App3.getFile('payloadFile.json')
		self.assertIsNotNone(file)

	def test_compareHash(self):
		samplePayload = '{"Name": "Test"}'
		samplePayload2 = '{"Name": "Test"}'
		hash1 = App3.hashPayload(samplePayload)
		hash2 = App3.hashPayload(samplePayload2)
		failCondition = False
		try:
			App3.compareHash(hash1, hash2)
		except:
			failCondition = True
		self.assertFalse(failCondition)

	def test_decodePayload(self):
		samplePayload = '{"Name": "Test"}'
		encodedSamplePayload = base64.b64encode(bytes(samplePayload, 'utf-8'))
		decodedPayload = App3.decodePayload(encodedSamplePayload)

		if (decodedPayload.decode('utf-8') == samplePayload):
			failCondition = False
		else:
			failCondition = True
		self.assertFalse(failCondition)

if __name__ == '__main__':
	unittest.main()
