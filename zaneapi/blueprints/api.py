import io

from quart import Blueprint, request, abort
from wand.image import Image

from ..imageops import magic, image_function, deepfry

bp = Blueprint('api', __name__)


@bp.route("/")
@bp.route("/status")
async def status():
    abort(200)


@bp.route("/magic", methods=["POST"])
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
