import redis
import os


class RedisConfig(object):
    r = None

    def __init__(self):
        self.r = None

    def get_connection(self):
        return self.r


class DevelopmentConfig(RedisConfig):

    def __init__(self):
        super(DevelopmentConfig, self).__init__()
        self.r = redis.StrictRedis(password=os.environ['REDIS_PASSWORD'], charset="utf-8", decode_responses=True)


class ProductionConfig(RedisConfig):

    def __init__(self):
        super(ProductionConfig, self).__init__()
        self.r = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)


def get_connection():
    if os.environ.get('ENV'):
        if os.environ.get('ENV') == 'dev':
            return DevelopmentConfig().get_connection()
        elif os.environ.get('ENV') == 'qa':
            import fakeredis
            return fakeredis.FakeStrictRedis(decode_responses=True)
    return ProductionConfig().get_connection()
