import time
import datetime
import json
from celery import Celery
from parser import XLSXParser
from repo import repo
app = Celery('tasks', broker='redis://redis:6379', backend='redis://redis:6379')


@app.task
def parse_diff(file_path, task_id):
    parser = XLSXParser(file_path)
    res = json.loads(repo.get(task_id))
    parse_result = parser.parse()
    res.update({"result": parse_result, "finished": str(datetime.datetime.now())})
    repo.set(task_id, json.dumps(res))

