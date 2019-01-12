import io

from quart import Blueprint, request, jsonify, make_response
from wand.image import Image

from ..imageops import image_function, magic, deepfry, invert

bp = Blueprint('api', __name__)


@bp.route("/")
@bp.route("/status")
async def status():
    response = await make_response(
        jsonify(
            {
                "code": 200,
                "message": "The API is functioning okay."
             }
        )
    )
    response.headers['Content-Type'] = "application/json"
    response.headers['Status'] = 200

    return response


@bp.route("/magic", methods=["POST"])
@bp.route("/magik", methods=["POST"])
async def magic_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, magic)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/deepfry", methods=["POST"])
async def deepfry_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, deepfry)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/invert", methods=["POST"])
@bp.route("/negate", methods=["POST"])
async def invert_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, invert)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response
