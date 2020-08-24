import unittest
import requests
import settings
import time


class TestUpload(unittest.TestCase):

    def test_health(self):
        response = requests.get(
            'http://172.17.0.1/health',
        )
        self.assertEqual(response.status_code, 200)

    def test_file_post(self):
        file_path = f'{settings.BASE_DIR}/data/example.xlsx'
        with open(file_path, 'rb') as test_file:
            response = requests.post(
                'http://172.17.0.1/upload',
                data=test_file
            )
        self.assertEqual(response.status_code, 201)
        job_id = response.json().get("job_id")
        time.sleep(2)
        response = requests.get(
            f'http://172.17.0.1/get/{job_id}',
        )
        self.assertEqual(response.json().get('status'), 'finished')

