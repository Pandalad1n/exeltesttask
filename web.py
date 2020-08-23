from flask import Flask, jsonify, request
import http
import uuid
import json
import datetime
from job import parse_diff
from pathlib import Path
from celery.result import AsyncResult
from job import app as celery_app
from repo import repo
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return '', http.HTTPStatus.OK


@app.route('/upload', methods=['POST'])
def upload():
    Path("/opt/source/").mkdir(parents=True, exist_ok=True)
    job_id = str(uuid.uuid4())
    with open(f'/opt/source/{job_id}.xlsx', 'wb+') as file:
        file.write(request.data)
    repo.set(job_id, json.dumps({"started": str(datetime.datetime.now())}))

    parse_diff.apply_async(tuple([f'/opt/source/{job_id}.xlsx', job_id]), task_id=job_id)
    return jsonify({"job_id": job_id}), http.HTTPStatus.CREATED


@app.route('/get/<job_id>', methods=['GET'])
def get(job_id):
    job = AsyncResult(job_id, app=celery_app)
    res = json.loads(repo.get(job_id))

    return jsonify(res)
