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
    repo.set(job_id, json.dumps({"started": str(datetime.datetime.now()), "status": "uploaded"}))

    parse_diff.apply_async(tuple([f'/opt/source/{job_id}.xlsx', job_id]), task_id=job_id)
    return jsonify({"job_id": job_id}), http.HTTPStatus.CREATED


@app.route('/get/<job_id>', methods=['GET'])
def get(job_id):
    job = AsyncResult(job_id, app=celery_app)
    try:
        job_status = job.status

        if job_status == "PENDING":
            job_status = "processing"
        if job_status == "FAILURE":
            job_status = "failed"
        if job_status == "SUCCESS":
            job_status = "finished"
    except Exception as err:
        job_status = "finished"

    res = json.loads(repo.get(job_id))
    parsed_result = res.get("result")
    if parsed_result:
        if parsed_result < 0:
            res.update({"added": abs(parsed_result)})
        else:
            res.update({"removed": abs(parsed_result)})
        res.pop("result")
    res.update({"status": job_status})
    return jsonify(res)
