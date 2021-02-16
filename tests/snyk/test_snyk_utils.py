import aiounittest
from unittest import mock

from app.snyk import utils



class TestSnykUtils(aiounittest.AsyncTestCase):
    def test_parse_project_name(self):
        project_name = 'org/project'
        res = utils.parse_project_name(project_name)
        self.assertEqual('project', res)

        project_name = 'org/_project'
        res = utils.parse_project_name(project_name)
        self.assertEqual('_project', res)

        project_name = 'org/_project:latest'
        res = utils.parse_project_name(project_name)
        self.assertEqual('_project', res)

        project_name = 'project:latest'
        res = utils.parse_project_name(project_name)
        self.assertEqual('project', res)


    def test_normalize_snyk_response(self):
        sample_data = {
            'name': 'test_name',
            'id': 'test_id'
        }

        res = utils.normalize(sample_data)
        self.assertEqual(res.name, 'test_name')
        self.assertEqual(res.id, 'test_id')

        sample_data = {
            'name': 'test_name',
            'id2': 'test_id'
        }

        res = utils.normalize(sample_data, 'id2')
        self.assertEqual(res.name, 'test_name')
        self.assertEqual(res.id, 'test_id')
