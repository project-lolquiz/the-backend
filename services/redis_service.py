from app import get_redis_connection

_redis = get_redis_connection()

def add():


def get_all():
    _redis.set('full stack', 'python')
    _redis.set('version', '3')
    _redis.set('framework', 'flask')
    keys = _redis.keys()
    return {keys[index]: _redis.get(keys[index]) for index in range(0, len(keys))}
