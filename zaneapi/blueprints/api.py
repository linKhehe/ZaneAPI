import io

from quart import Blueprint, request, abort
from wand.image import Image

from ..imageops import image_function, magic, deepfry, invert

bp = Blueprint('api', __name__)


@bp.route("/")
@bp.route("/status")
async def status():
    abort(200)


@bp.route("/magic", methods=["POST"])
@bp.route("/magik", methods=["POST"])
async def magic_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, magic)

    assert isinstance(image, io.BytesIO)

    return image.getvalue()


@bp.route("/deepfry", methods=["POST"])
async def deepfry_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, deepfry)

    assert isinstance(image, io.BytesIO)

    return image.getvalue()


@bp.route("/invert", methods=["POST"])
@bp.route("/negate", methods=["POST"])
async def invert_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, invert)

    assert isinstance(image, io.BytesIO)

    return image.getvalue()
