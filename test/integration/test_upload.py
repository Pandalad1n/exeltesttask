import unittest
import requests
import settings
import time
import base64
from requests.auth import HTTPBasicAuth


class TestUpload(unittest.TestCase):

    def test_health(self):
        response = requests.get(
            'http://172.17.0.1/health',
        )
        self.assertEqual(response.status_code, 200)

    def _auth_headers(self):
        return {
            "Authorization": 'Basic ' + base64.b64encode(
                (settings.LOGIN + ':' + settings.PASSWORD).encode('utf-8')).decode('utf-8')
        }

    def test_post_unauthorised_returns_401(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        with open(file_path, 'rb') as test_file:
            response = requests.post(
                'http://172.17.0.1/upload',
                data=test_file
            )
        self.assertEqual(response.status_code, 401)

    def test_post_happy_path(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        with open(file_path, 'rb') as test_file:
            response = requests.post(
                'http://172.17.0.1/upload',
                data=test_file,
                auth=HTTPBasicAuth(settings.PASSWORD, settings.LOGIN)
            )
        self.assertEqual(response.status_code, 201)
        job_id = response.json().get("job_id")
        time.sleep(2)
        response = requests.get(
            f'http://172.17.0.1/get/{job_id}',
            auth=HTTPBasicAuth(settings.PASSWORD, settings.LOGIN)
        )
        self.assertEqual(response.json().get('status'), 'finished')
