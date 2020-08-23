import unittest
from web import app
import http
from unittest.mock import patch, mock_open


class TestWeb(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.client = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_file_post(self):
        with patch('web.open', mock_open()) as mock:
            response = self.client.post('/upload', data=b'test')
            self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
            self.assertEqual(response.json, {"job_id": response.json.get("job_id")})
            mock.assert_called_once_with(f'/opt/source/{response.json.get("job_id")}', 'w+')
            mock().write.assert_called_once_with(b'test')
