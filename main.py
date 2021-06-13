from flask import make_response, jsonify
from jsonschema import ValidationError

from app import create_app
from routes.default_route import default_rest
from routes.dumb_route import dumb_rest
from routes.game_route import game_config_rest
from routes.user_route import user_rest
from routes.rooms.room_route import room_rest
from routes.games.game_route import game_rest

default_prefix = '/lolquiz'

app = create_app(default_prefix)
app.register_blueprint(default_rest)
app.register_blueprint(dumb_rest, url_prefix=default_prefix)
app.register_blueprint(game_config_rest, url_prefix=default_prefix)
app.register_blueprint(game_rest, url_prefix=default_prefix)
app.register_blueprint(user_rest, url_prefix=default_prefix)
app.register_blueprint(room_rest, url_prefix=default_prefix)


@app.errorhandler(404)
def http_not_found(e):
    print(e)
    return "<strong>It seems this is not correct :-(</strong>", 404


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    return error  # handle other "Bad Request"-errors


if __name__ == '__main__':
    app.run()
