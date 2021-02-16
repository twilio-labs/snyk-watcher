import aiounittest
import copy
import pydantic

from app.github.webhook_model import Webhook

data = {
    "action": 'renamed',
    "pull_request": {
            "merged": True
    },
    "repository": {
        "full_name": "organization/project",
        "lastName": "p",
        "age": 71
    },
    "changes": {
        "repository": {
            "name": {
                "from": 'project2'
            }
        }
    }
}

data2 = {
    "action": 'created',
    "repository": {
        "full_name": "organization/project",
        "lastName": "p",
        "age": 71
    }
}

class TestWebhookValidator(aiounittest.AsyncTestCase):
    def test_good_import(self):
        local_data = copy.deepcopy(data2)
        event = Webhook(**local_data)

        self.assertTrue(event.requires_import())
        self.assertEqual(False, event.requires_delete())

    def test_good_delete(self):
        local_data = copy.deepcopy(data2)
        local_data['action'] = 'deleted'
        event = Webhook(**local_data)

        self.assertTrue(event.requires_delete())
        self.assertEqual(False, event.requires_import())

    def test_good_renamed(self):
        local_data = copy.deepcopy(data)
        event = Webhook(**local_data)

        self.assertTrue(event.requires_delete())
        self.assertTrue(event.requires_import())

    def test_repo_name(self):
        local_data = copy.deepcopy(data2)
        local_data['repository']['full_name'] = ''
        threw = False

        try:
            event = Webhook(**local_data)
        except pydantic.ValidationError as e:
            threw = True

        self.assertTrue(threw)