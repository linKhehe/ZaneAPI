from quart import Blueprint, request, jsonify, make_response
from wand.color import Color

from ..imageops import *

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


@bp.route("/desat", methods=["POST"])
@bp.route("/desaturation", methods=["POST"])
async def desat_endpoint():
    threshold = int(request.args.get("threshold") or 2)
    image = Image(blob=await request.body)
    image = await image_function(image, desat, threshold)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/sat", methods=["POST"])
@bp.route("/saturation", methods=["POST"])
async def sat_endpoint():
    threshold = int(request.args.get("threshold") or 1)
    image = Image(blob=await request.body)
    image = await image_function(image, sat, threshold)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response
    

@bp.route("/colormap", methods=["POST"])
async def colormap_endpoint():
    color_arg = f'#{((request.args.get("color") or "7289DA").replace("0x", "#").lstrip("#")):0>6}'
    color_obj = Color(color_arg)
    rgb = color_obj.red_int8, color_obj.green_int8, color_obj.blue_int8
    image = PILImage.open(io.BytesIO(await request.body))
    transformed = await image_function(image, colormap, rgb)
    
    assert isinstance(transformed, io.BytesIO)
    
    response = await make_response(transformed.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"
    
    return response
    

@bp.route("/noise", methods=["POST"])
async def noise_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, noise)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

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


@bp.route("/arc", methods=["POST"])
async def arc_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, arc)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/concave", methods=["POST"])
async def concave_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, concave)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/convex", methods=["POST"])
async def convex_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, convex)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/floor", methods=["POST"])
async def floor_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, floor)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/blur", methods=["POST"])
async def blur_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, blur)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/vaporwave", methods=["POST"])
async def vaporwave_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, vaporwave)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/emboss", methods=["POST"])
async def emboss_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, emboss)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/shade", methods=["POST"])
async def shade_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, shade)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/edge", methods=["POST"])
async def edge_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, edge)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/bend", methods=["POST"])
async def bend_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, bend)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/posterize", methods=["POST"])
async def posterize_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, posterize)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response


@bp.route("/grayscale", methods=["POST"])
async def grayscale_endpoint():
    image = Image(blob=await request.body)
    image = await image_function(image, grayscale)

    assert isinstance(image, io.BytesIO)

    response = await make_response(image.getvalue())
    response.headers['Status'] = 200
    response.headers['Content-Type'] = "image/png"

    return response
