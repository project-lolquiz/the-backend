import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


def get_config():
    if os.environ.get('ENV') and os.environ.get('ENV') == 'dev':
        return DevelopmentConfig()
    return ProductionConfig()
