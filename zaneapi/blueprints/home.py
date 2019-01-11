import random

from quart import Blueprint, render_template

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET"])
async def index():
    messages = ["My favorite meal is RAM.", "It hurts.", "Please stop.", "ir3/linK is my dad."]

    return await render_template(
        "index.html",
        message=random.choice(messages)
    )
