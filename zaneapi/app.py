import requests
import flask

from . import exceptions, redis


def create_app(config):
    app = flask.Flask(__name__)
    app.config.from_object(config)

    app.redis = redis.create_redis(app.config["DATABASE_KWARGS"])

    with app.app_context():
        from .blueprints import api, auth, index, projects

        app.register_blueprint(api.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(index.bp)
        app.register_blueprint(projects.bp)

    @app.errorhandler(exceptions.Banned)
    def banned(_):
        return "<h1 style='color: red;'>BANNED</h1>"

    @app.errorhandler(requests.exceptions.ConnectionError)
    def invalid_url(_):
        return flask.jsonify({"code": 400, "message": "Failed to establish connection to the provided address."}), 400

    @app.errorhandler(requests.exceptions.MissingSchema)
    def invalid_uri(exception):
        return flask.jsonify({"code": 400, "message": str(exception)}), 400

    @app.errorhandler(exceptions.Unauthorized)
    def invalid_token(_):
        return flask.jsonify({"code": 403, "message": "Unauthorized"}), 403

    return app
