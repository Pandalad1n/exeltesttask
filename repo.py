import redis
import json
import settings


class Repo:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_ADDR, port=settings.REDIS_PORT, db=0)

    def update(self, job_id, data):
        res = json.loads(self.redis.get(job_id) or '{}')
        res.update(data)
        self.redis.set(job_id, json.dumps(res))

    def get(self, job_id):
        return json.loads(self.redis.get(job_id) or '{}')

repo = Repo()
