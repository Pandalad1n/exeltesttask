from flask import Flask, jsonify, request
import http
import uuid
import json
import datetime
import base64
import settings
from job import parse_diff
from pathlib import Path
from celery.result import AsyncResult
from job import app as celery_app
from repo import repo
app = Flask(__name__)


def auth_required(func):
    def wrapper(*args, **kwargs):
        try:
            encoded_login = request.headers['Authorization'].split(' ')[1]
            login, password = base64.b64decode(encoded_login.encode('utf-8')).decode('utf-8').split(':')
            assert login == settings.LOGIN
            assert password == settings.PASSWORD
        except (KeyError, IndexError):
            return '', http.HTTPStatus.UNAUTHORIZED
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/health', methods=['GET'])
def health():
    return '', http.HTTPStatus.OK


@app.route('/upload', methods=['POST'])
@auth_required
def upload():
    Path("/opt/source/").mkdir(parents=True, exist_ok=True)
    job_id = str(uuid.uuid4())
    with open(f'/opt/source/{job_id}.xlsx', 'wb+') as file:
        file.write(request.data)
    repo.update(job_id, {"created": str(datetime.datetime.now()), "status": "uploaded"})

    parse_diff.apply_async([f'/opt/source/{job_id}.xlsx', job_id], task_id=job_id)
    return jsonify({"job_id": job_id}), http.HTTPStatus.CREATED


@app.route('/get/<job_id>', methods=['GET'])
@auth_required
def get(job_id):
    statuses = {
        "PENDING": "processing",
        "FAILURE": "failed",
        "SUCCESS": "finished",
    }
    job = repo.get(job_id)
    if not job:
        return '', http.HTTPStatus.NOT_FOUND

    if 'result' not in job:
        res = AsyncResult(job_id, app=celery_app)
        job.update({'status': statuses.get(res.status, "unknown")})
        return jsonify(job)

    job.update({
        'added' if job['result'] < 0 else 'removed': abs(job['result']),
        'status': 'finished',
    })
    job.pop('result')
    return jsonify(job)
