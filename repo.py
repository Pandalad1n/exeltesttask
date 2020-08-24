import redis
import json


class Repo:
    def __init__(self):
        # TODO: from config
        self.redis = redis.Redis(host='redis', port=6379, db=0)

    def update(self, job_id, data):
        res = json.loads(self.redis.get(job_id) or '{}')
        res.update(data)
        self.redis.set(job_id, json.dumps(res))

    def get(self, job_id):
        return json.loads(self.redis.get(job_id) or '{}')

repo = Repo()
