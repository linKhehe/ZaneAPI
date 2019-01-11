from quart import Quart, render_template, jsonify

from .blueprints import api, home

zane = Quart(__name__)

zane.register_blueprint(api.bp, "/api")
zane.register_blueprint(home.bp, "/")
