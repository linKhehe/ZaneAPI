import base64
import io

from flask import Blueprint, request, make_response

from .. import imageops


bp = Blueprint("api", __name__)


valid_ops = ["magic", "deepfry", "emboss",
             "vaporwave", "floor", "concave",
             "convex", "invert", "lsd",
             "posterize", "grayscale", "bend",
             "edge", "gay", "sort",
             "sobel", "shuffle", "swirl",
             "polaroid", "arc"]


def decode(image_encoded: str) -> io.BytesIO:
    image_decoded = base64.b64decode(image_encoded)
    image_bytes = io.BytesIO(image_decoded)
    image_bytes.seek(0)

    return image_bytes


def encode(image_bytes: io.BytesIO) -> str:
    image_value = image_bytes.getvalue()
    image_encoded = base64.b64encode(image_value)

    return image_encoded.decode('ascii')


def response(status: int = 200, message: str = "success", **kwargs) -> dict:
    return dict(status=status, message=message, **kwargs)


@bp.route("/<string:op>", methods=["POST"])
def manipulation(op: str):
    if op not in valid_ops:
        return response(status=400, message="Invalid image operation")

    image = request.json.get("image")
    if image is None:
        return response(status=400, message="Missing image argument.")

    image = decode(image)
    image = getattr(imageops, op)(image)

    return response(image=encode(image))
