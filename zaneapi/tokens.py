import base64
import functools
import secrets

from flask import current_app, request

from .exceptions import Unauthorized


class Token:

    def __init__(self, redis, project_id):
        self._redis = redis
        self.project_id = project_id

    def revoke(self):
        self._redis.hdel(self.project_id, "token")

    def generate(self):
        token_identifier = base64.b64encode(str(self.project_id).encode()).decode()
        token_security = secrets.token_urlsafe(36).replace('.', '_')

        token = token_identifier + "." + token_security

        self._redis.hset(self.project_id, "token", token)

    def get(self):
        token = self._redis.hget(self.project_id, "token")

        if token is None:
            return None
        return token.decode()

    def __str__(self):
        return self.get()


def validate_token(token: str) -> bool:
    try:
        app_id = base64.b64decode(token.split(".")[0].encode()).decode()
    except:
        return False

    correct_token = current_app.redis.hget(app_id, "token")

    if correct_token is None:
        return False

    if token == correct_token.decode():
        return True


def requires_token(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        token = request.args.get("token", request.headers.get("Authorization"))

        if token is None or not validate_token(token):
            raise Unauthorized

        current_app.redis.incr("usage")

        return view(*args, **kwargs)
    return wrapper
