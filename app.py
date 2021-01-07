from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configs.db_config import get_config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    return app


def get_db_connection():
    return db
