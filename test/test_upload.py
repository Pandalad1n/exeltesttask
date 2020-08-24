import unittest
from web import app
import http
import base64
import settings
from unittest.mock import patch, mock_open, ANY


class TestWeb(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.client = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def _auth_headers(self):
        return {
                "Authorization": 'Basic ' + base64.b64encode((settings.LOGIN + ':' + settings.PASSWORD).encode('utf-8')).decode('utf-8')
            }

    def test_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_post_unauthorised_returns_401(self):
        response = self.client.post('/upload', data=b'test')
        self.assertEqual(response.status_code, http.HTTPStatus.UNAUTHORIZED)

    @patch('web.parse_diff')
    @patch('web.repo')
    def test_post_happy_path(self, m_repo, m_parse):
        with patch('web.open', mock_open()) as m_open:
            response = self.client.post('/upload', data=b'test', headers=self._auth_headers())
            self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
            job_id = response.json.get("job_id")
            self.assertEqual(response.json, {"job_id": job_id})
            m_open.assert_called_once_with(f'/opt/source/{job_id}.xlsx', 'wb+')
            m_open().write.assert_called_once_with(b'test')
            m_repo.update.assert_called_once_with(job_id, {"status": "uploaded", 'created': ANY})
            m_parse.apply_async.assert_called_once_with([f'/opt/source/{job_id}.xlsx', job_id], task_id=job_id)
