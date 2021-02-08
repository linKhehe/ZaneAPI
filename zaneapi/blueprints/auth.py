import flask
from flask import current_app, session, request

from .. import oauth

bp = flask.Blueprint("auth", __name__)


@bp.route("/login")
def login():
    discord = oauth.create_session(scope=current_app.config["OAUTH2_SCOPES"])
    authorization_url, state = discord.authorization_url(oauth.AUTHORIZATION_BASE_URL)

    session["oauth2_state"] = state

    return flask.redirect(authorization_url)


@bp.route("/callback")
def callback():
    if request.values.get("error"):
        return request.values["error"]

    discord = oauth.create_session(state=session.get("oauth2_state"))
    token = discord.fetch_token(
        oauth.TOKEN_URL,
        client_secret=oauth.OAUTH2_CLIENT_SECRET,
        authorization_response=request.url
    )

    session["oauth2_token"] = token
    session["discord_user_data"] = discord.get(oauth.API_BASE_URL + '/users/@me').json()

    user = oauth.get_user()
    user.save(**session["discord_user_data"])

    return flask.redirect("/")


@bp.route("/logout")
def logout():
    session.clear()
    return flask.redirect("/")
