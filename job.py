import datetime
import settings
from celery import Celery
from parser import XLSXParser
from repo import repo

app = Celery('tasks', broker=f'redis://{settings.REDIS_ADDR}:{settings.REDIS_PORT}')


@app.task
def parse_diff(file_path, task_id):
    parser = XLSXParser(file_path)
    parse_result = parser.parse()
    repo.update(task_id, {"result": parse_result, "finished": str(datetime.datetime.now())})
