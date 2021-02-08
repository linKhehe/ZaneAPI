import functools
import os
import time

import flask
from flask import session
from requests_oauthlib import OAuth2Session

from .user import User
from .exceptions import Banned

app = flask.current_app

OAUTH2_CLIENT_ID = app.config["OAUTH2_CLIENT_ID"]
OAUTH2_CLIENT_SECRET = app.config["OAUTH2_CLIENT_SECRET"]
OAUTH2_REDIRECT_URI = app.config["OAUTH2_CALLBACK_URL"]

API_BASE_URL = "https://discordapp.com/api"
AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"

app.config["SECRET_KEY"] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def create_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            "client_id": OAUTH2_CLIENT_ID,
            "client_secret": OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=lambda t: session.update("oauth2_token", t)
    )


def get_user():
    if session.get("discord_user_data") is None:
        return None

    user = User(flask.current_app.redis, **session.get("discord_user_data"))

    if not user.is_registered():
        discord = create_session(token=session.get("oauth2_token"))
        resp = discord.get(API_BASE_URL + '/users/@me')

        if not resp.ok:
            return None

        data = resp.json()
        data["is_banned"] = False
        data["is_admin"] = False

        return user.register(**data)

    if user.is_banned:
        raise Banned

    return user


def requires_user(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        user = get_user()

        if user is None:
            return flask.redirect("/login")

        return view(user, *args, **kwargs)
    return wrapper
