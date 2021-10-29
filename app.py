from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

from configs.db_config import get_connection as db_connection
from configs.redis_config import get_connection as redis_connection


db = SQLAlchemy()
_redis = redis_connection()


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s.%(funcName)s[%(lineno)d]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Lolquiz API",
        "description": "API for Lolquiz",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "",
            "url": "",
        },
        "termsOfService": "tof",
        "version": "0.0.1"
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}


def create_app(default_prefix):
    app = Flask(__name__)
    app.config.from_object(db_connection())
    db.init_app(app)
    swagger_config['url_prefix'] = default_prefix
    Swagger(app, template=swagger_template, config=swagger_config)
    return app


def get_db_connection():
    return db


def get_redis_connection():
    return _redis
