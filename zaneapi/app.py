from flask import Flask


def create_app(config):
    """Create an instance of the Flask application."""
    app = Flask(__name__)

    app.config.from_object(config)

    from .blueprints import api

    app.register_blueprint(api.bp, url_prefix="/api")

    return app
