import redis
import os

r = redis.StrictRedis(password=os.environ['REDIS_PASSWORD'], charset="utf-8", decode_responses=True)


def get_all():
    r.set('full stack', 'python')
    r.set('version', '3')
    r.set('framework', 'flask')
    keys = r.keys()
    return {keys[index]: r.get(keys[index]) for index in range(0, len(keys))}
