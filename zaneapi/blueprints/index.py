import flask

from .. import oauth

bp = flask.Blueprint("index", __name__)


@bp.route("/")
def index():
    return flask.render_template("index.html", user=oauth.get_user())
