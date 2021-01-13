from app import create_app
from routes.default_route import default_rest
from routes.dumb_route import dumb_rest
from routes.user_route import user_rest

default_prefix = '/lolquiz'

app = create_app()
app.register_blueprint(default_rest)
app.register_blueprint(dumb_rest, url_prefix=default_prefix)
app.register_blueprint(user_rest, url_prefix=default_prefix)


@app.errorhandler(404)
def http_not_found(e):
    print(e)
    return "<strong>It seems this is not correct :-(</strong>", 404


if __name__ == '__main__':
    app.run()
