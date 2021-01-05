from flask import Flask

from services.redis_client import get_all

app = Flask(__name__)


@app.route('/')
@app.route('/ping')
def ping():
    print("I'am online!!!")
    return "pong", 200


@app.route('/redis-get-all')
def redis_get_all():
    return get_all(), 200


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<strong>It seems this is not correct :-(</strong>", 404


if __name__ == '__main__':
    app.run()
