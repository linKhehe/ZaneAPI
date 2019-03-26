import imageops
import io

bp = Blueprint('api', __name__)


async def add_headers(response, content_type: str, status: int):
    response.headers['Content-Type'] = content_type
    response.headers['Status'] = status

    return response

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
    return await add_headers(response, "application/json", 200)


@bp.route("/desat", methods=["POST"])
@bp.route("/desaturation", methods=["POST"])
async def desat_endpoint():
    threshold = int(request.args.get("threshold") or 2)

    response = await make_response(await imageops.desat(io.BytesIO(await request.body), threshold).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/sat", methods=["POST"])
@bp.route("/saturation", methods=["POST"])
async def sat_endpoint():
    threshold = int(request.args.get("threshold") or 1)
    
    response = await make_response(await imageops.sat(io.BytesIO(await request.body), threshold).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/noise", methods=["POST"])
async def noise_endpoint():
    response = await make_response(await imageops.noise(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/magic", methods=["POST"])
@bp.route("/magik", methods=["POST"])
async def magic_endpoint():
    response = await make_response(await imageops.magic(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/deepfry", methods=["POST"])
async def deepfry_endpoint():
    response = await make_response(await imageops.deepfry(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/invert", methods=["POST"])
@bp.route("/negate", methods=["POST"])
async def invert_endpoint():
    response = await make_response(await imageops.invert(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/arc", methods=["POST"])
async def arc_endpoint():
    response = await make_response(await imageops.arc(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/concave", methods=["POST"])
async def concave_endpoint():
    response = await make_response(await imageops.concave(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/convex", methods=["POST"])
async def convex_endpoint():
    response = await make_response(await imageops.convex(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/floor", methods=["POST"])
async def floor_endpoint():
    response = await make_response(await imageops.floor(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/blur", methods=["POST"])
async def blur_endpoint():
    response = await make_response(await imageops.blur(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/vaporwave", methods=["POST"])
async def vaporwave_endpoint():
    response = await make_response(await imageops.vaporwave(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/emboss", methods=["POST"])
async def emboss_endpoint():
    response = await make_response(await imageops.emboss(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/shade", methods=["POST"])
@bp.route("/sobel", methods=["POST"])
async def shade_endpoint():
    response = await make_response(await imageops.sobel(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/edge", methods=["POST"])
async def edge_endpoint():
    response = await make_response(await imageops.edge(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/bend", methods=["POST"])
async def bend_endpoint():
    response = await make_response(await imageops.bend(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/posterize", methods=["POST"])
async def posterize_endpoint():
    response = await make_response(await imageops.posterize(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/grayscale", methods=["POST"])
async def grayscale_endpoint():
    response = await make_response(await imageops.greyscale(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/lsd", methods=["POST"])
async def lsd_endpoint():
    response = await make_response(await imageops.lsd(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/sort", methods=["POST"])
async def sort_endpoint():
    response = await make_response(await imageops.sort(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/gay", methods=["POST"])
async def gay_endpoint():
    response = await make_response(await imageops.gay(io.BytesIO(await request.body)).getvalue())
    return await add_headers(response, "image/png", 200)


@bp.route("/ascii", methods=["POST"])
async def ascii_endpoint():
    response = await make_response(jsonify({"ascii": await imageops.ascii(io.BytesIO(await request.body))}))
    return await add_headers(response, "application/json", 200)
