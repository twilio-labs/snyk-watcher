import aiounittest
from app.github import webhook_validator

secret = 'SECRET'

payload_hash = '93a95e9f9dccd84f6789689e952b54a5575b1f34'

sample_payload = {
    "action": "added",
    "repository": {
        "full_name": 'organization/project'
    }
}

class TestWebhookValidator(aiounittest.AsyncTestCase):
    def test_sign_payload(self):
        payload = str(sample_payload).encode('utf-8')
        signature = webhook_validator.sign_payload(payload, secret)
        self.assertEqual(payload_hash, signature)

        payload = (str(sample_payload) + '1').encode('utf-8')
        signature = webhook_validator.sign_payload(payload, secret)

        self.assertNotEqual(payload_hash, signature)


    def test_exctract_signature(self):
        """
        This should fail for anything other than a sha1
        in the following format
        sha1=hash
        """
        test = webhook_validator.extract_signature('sha1=hash')
        self.assertEqual('hash', test)

        test = webhook_validator.extract_signature('hash')
        self.assertEqual('', test)

        test = webhook_validator.extract_signature('sha=hash')
        self.assertEqual('', test)


    def test_verify_webhook(self):
        payload = str(sample_payload).encode('utf-8')
        signature = 'sha1=' + payload_hash
        
        res = webhook_validator.verify_webhook(payload, signature, secret)
        self.assertEqual(res, True)

        res = webhook_validator.verify_webhook(payload, payload_hash, secret)
        self.assertEqual(res, False)

        res = webhook_validator.verify_webhook(payload, signature, 'WRONG_SECRET')
        self.assertEqual(res, False)
