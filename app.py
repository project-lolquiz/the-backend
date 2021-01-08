from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configs.db_config import get_config as db_config
from configs.redis_config import RedisConfig

db = SQLAlchemy()
_redis = RedisConfig()


def create_app():
    app = Flask(__name__)
    app.config.from_object(db_config())
    db.init_app(app)
    return app


def get_db_connection():
    return db


def get_redis_connection():
    return _redis.get_connection()
