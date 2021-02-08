import functools

import math
import numpy as np
import flask
import PIL
import requests
import skimage
import skimage.exposure
import skimage.filters
import wand
import wand.image
import wand.color
from flask import current_app, request
from skimage.color.adapt_rgb import adapt_rgb, each_channel

from ..image_managers import Numpy, Pillow, Wand
from ..tokens import requires_token, validate_token

bp = flask.Blueprint("api", __name__, url_prefix="/api")


@bp.route("/user_count")
def user_count():
    count = current_app.redis.get("user_count").decode()
    return flask.jsonify({"user_count": int(count)})


@bp.route("/usage_count")
def usage_count():
    count = current_app.redis.get("usage_count").decode()
    return flask.jsonify({"usage_count": int(count)})


@bp.route("/auth")
def auth():
    token = request.args.get("token", request.headers.get("Authorization"))
    return flask.jsonify({"valid": validate_token(token)})


def image_endpoint(img_manager, skip_output=False):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            url = request.args.get("url")

            img_bytes = requests.get(url).content
            img_object = img_manager.input(img_bytes)

            if skip_output:
                return view(img_object, *args, **kwargs)

            img_object, filename = view(img_object, *args, **kwargs)

            img = img_manager.output(img_object)
            return flask.send_file(img, attachment_filename=filename)
        return wrapper
    return decorator


def clamp(n, low, high):
    if n < low:
        return low
    elif n > high:
        return high
    return n


def content_aware_scale(img, magnitude) -> wand.image.Image:
    scale_min = 1.0 - magnitude
    scale_max = 1.0 + magnitude

    img.liquid_rescale(
        width=int(img.width * scale_min),
        height=int(img.height * scale_min),
        delta_x=1,
        rigidity=0
    )
    img.liquid_rescale(
        width=int(img.width * scale_max),
        height=int(img.height * scale_max),
        delta_x=2,
        rigidity=0
    )

    return img


@bp.route("/magic")
@requires_token
@image_endpoint(Wand)
def magic(img):
    img.sample(256, 256)

    output = wand.image.Image(width=img.width, height=img.height)
    output.format = "GIF"

    output.sequence[0] = img
    del output.sequence[1:]
    output.sequence.extend(img for _ in range(0, 2))

    for magnitude in range(1, int(clamp(float(request.args.get("magnitude", 0.6)), 0.1, 2) * 10)):
        with img.clone() as frame:
            content_aware_scale(frame, magnitude / 10)
            frame.sample(256, 256)
            output.sequence.append(frame)

    output.sequence.extend(output.sequence[-1] for _ in range(0, 4))
    output.sequence.extend(reversed(output.sequence))

    img.close()

    return output, "magic.gif"


@bp.route("/floor")
@requires_token
@image_endpoint(Wand)
def floor(img):
    img.sample(256, 256)

    output = wand.image.Image(width=img.width, height=img.height, background=wand.color.Color("transparent"))
    output.format = "GIF"
    output.dispose = "background"

    del output.sequence[0]

    w, h = img.width, img.height

    for p in np.linspace(0, math.pi, 13):
        p = -0.5 * math.cos(p) + 0.5

        with img.clone() as frame:
            frame.virtual_pixel = "mirror"
            frame.dispose = "background"
            frame.distort(
                method="bilinear_reverse",
                arguments=(
                    0, 0, .3 * w * p, .85 * h * p,             # src1x, src1y, dst1x, dst1y,
                    w, 0, w - (w * p * .3), .85 * h * p,       # src2x, src2y, dst2x, dst2y,
                    0, h, .15 * w * p, h - (h * p * .1),       # src3x, src3y, dst3x, dst3y,
                    w, h, w - (w * p * .15), h - (h * p * .1)  # src4x, src4y, dst4x, dst4y
                )
            )
            output.sequence.append(frame)

    img.close()

    output.sequence.extend(reversed(output.sequence))
    return output, "floor.gif"


@bp.route("/braille")
@requires_token
@image_endpoint(Pillow, skip_output=True)
def braille(img):
    braille_order = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3))

    img = img.resize((57 * 2, 34 * 4))
    img = img.convert("1")

    img = np.array(img)

    art = []
    for y in range(0, img.shape[0], 4):
        row = []
        for x in range(0, img.shape[1], 2):
            pattern = "".join(str(int(img[y + oy][x + ox])) for ox, oy in reversed(braille_order))
            row.append(chr(0x2800 + int(pattern if pattern != "00000000" else "10000000", 2)))
        art.append(row)

    return "\n".join("".join(row) for row in art)


@bp.route("/deepfry")
@requires_token
@image_endpoint(Wand)
def deepfry(img):
    img.format = "jpeg"
    img.compression_quality = 1
    img.modulate(saturation=700)
    return img, "deepfry.png"


@bp.route("/dots")
@requires_token
@image_endpoint(Wand)
def dots(img):
    img.transform_colorspace('gray')
    img.ordered_dither('h16x16o')

    return img, "dots.png"


@bp.route("/jpeg")
@requires_token
@image_endpoint(Wand)
def jpeg(img):
    img.format = "jpeg"
    img.compression_quality = 1

    return img, "jpeg.png"


@bp.route("/spread")
@requires_token
@image_endpoint(Wand)
def spread(img):
    img.resize(256, 256)
    img.alpha_channel = False

    output = wand.image.Image(width=img.width, height=img.height)
    output.format = "GIF"

    output.sequence[0] = img
    output.sequence.extend(img for _ in range(0, 2))

    for radius in range(0, 13):
        with img.clone() as frame:
            frame.spread(radius=radius ** 2)
            output.sequence.append(frame)

    output.sequence.extend(reversed(output.sequence))

    img.close()

    output.optimize_layers()
    output.optimize_transparency()

    return output, "spread.gif"


@bp.route("/cube")
@requires_token
@image_endpoint(Wand)
def cube(image):
    def s(x):
        return int(x / 3)

    image.resize(s(1000), s(860))
    image.format = "png"
    image.alpha_channel = 'opaque'

    image1 = image
    image2 = wand.image.Image(image1)

    out = wand.image.Image(width=s(3000 - 450), height=s(860 - 100) * 3)
    out.format = "png"

    image1.shear(background=wand.color.Color("none"), x=-30)
    image1.rotate(-30)
    out.composite(image1, left=s(500 - 250), top=s(0 - 230) + s(118))
    image1.close()

    image2.shear(background=wand.color.Color("rgba(0,0,0,0)"), x=30)
    image2.rotate(-30)
    image3 = wand.image.Image(image2)
    out.composite(image2, left=s(1000 - 250) - s(72), top=s(860 - 230))
    image2.close()

    image3.flip()
    out.composite(image3, left=s(0 - 250) + s(68), top=s(860 - 230))
    image3.close()

    out.crop(left=80, top=40, right=665, bottom=710)

    return out, "cube.png"


@bp.route("/sort")
@requires_token
@image_endpoint(Numpy)
def sort(img):
    shape = img.shape
    img = img.reshape((img.shape[0] * img.shape[1], img.shape[2]))
    img = np.sort(img, 0)
    return img.reshape(shape), "sort.png"


@bp.route("/palette")
@requires_token
@image_endpoint(Pillow)
def palette(img):
    color_width = 128
    width = int((512 / img.height) * img.width)

    img = img.resize((width, 512))
    colors = colorgram.extract(img, 8)

    new_img = PIL.Image.new(img.mode, (width + color_width, 512))
    draw = PIL.ImageDraw.Draw(new_img)
    font = PIL.ImageFont.truetype("zane_api/static/JetBrainsMono-Regular.ttf", 30)

    for i, color in enumerate(colors):
        draw.rectangle([(0, i * 64), (128, (i + 1) * 64)], fill=color.rgb)
        draw.text((0, i * 64), f"#{color.rgb[0]:02x}{color.rgb[1]:02x}{color.rgb[2]:02x}", font=font, fill=(*tuple(abs(255 - c) for c in color.rgb), 255))

    new_img.paste(img, box=(color_width, 0))
    img.close()
    return new_img, "palette.png"


@bp.route("/invert")
@requires_token
@image_endpoint(Wand)
def invert(img) -> wand.image.Image:
    img.alpha_channel = False
    img.negate()
    return img, "inverted.png"


@bp.route("/posterize")
@requires_token
@image_endpoint(Wand)
def posterize(img) -> wand.image.Image:
    img.posterize(2)
    return img, "posterized.png"


@bp.route("/grayscale")
@requires_token
@image_endpoint(Wand)
def grayscale(img) -> wand.image.Image:
    img.transform_colorspace('gray')
    return img, "grayscale.png"


@bp.route("/pixelate")
@requires_token
@image_endpoint(Wand)
def pixelate(img):
    original_size = (img.width, img.height)
    scale = clamp(request.args.get("scale", 0.3), 0.1, 1)

    img.resize(
        int(img.width * scale),
        int(img.height * scale),
        blur=0, filter="box"
    )
    img.resize(*original_size, blur=0, filter="box")
    return img, "pixelated.png"


@bp.route("/swirl")
@requires_token
@image_endpoint(Wand)
def swirl(img):
    img.sample(256, 256)

    output = wand.image.Image(width=img.width, height=img.height)
    output.format = "GIF"
    output.alpha_channel = "off"

    for i, a in enumerate(np.linspace(0, math.pi * 2, 45)):
        with img.clone() as frame:
            frame.swirl(math.sin(a) * int(request.args.get("angle", 280)))
            try:
                output.sequence[i] = frame
            except:
                output.sequence.append(frame)

    img.close()
    return output, "swirl.gif"


@bp.route("/sobel")
@requires_token
@image_endpoint(Numpy)
def sobel(img):
    @adapt_rgb(each_channel)
    def sobel_each(image):
        return skimage.filters.sobel(image)
    return skimage.exposure.rescale_intensity(255 - sobel_each(img) * 255), "sobel.png"


@bp.route("/rotate")
@requires_token
@image_endpoint(Wand)
def rotate(img):
    img.rotate(int(request.args.get("degree", 0)))
    return img, "rotated.png"


@bp.route("/resize")
@requires_token
@image_endpoint(Wand)
def resize(img):
    w = clamp(int(request.args.get("width", img.width)), 1, 9999)
    h = clamp(int(request.args.get("height", img.height)), 1, 9999)

    img.resize(w, h)

    return img, "resized.png"


@bp.route("/color_ascii")
@requires_token
@image_endpoint(Pillow, skip_output=True)
def color_ascii(img):
    colors = {
        "\N{BLACK LARGE SQUARE}": (56, 56, 56),
        "\N{WHITE LARGE SQUARE}": (242, 242, 242),
        "\N{LARGE RED SQUARE}": (232, 18, 36),
        "\N{LARGE GREEN SQUARE}": (22, 198, 12),
        "\N{LARGE BLUE SQUARE}": (0, 120, 215),
        "\N{LARGE ORANGE SQUARE}": (247, 99, 12),
        "\N{LARGE YELLOW SQUARE}": (255, 241, 0),
        "\N{LARGE BROWN SQUARE}": (142, 86, 46),
        "\N{LARGE PURPLE SQUARE}": (136, 108, 228),
        "\N{SQUARED SOS}": (240, 58, 23),
        "\N{SQUARED CJK UNIFIED IDEOGRAPH-7533}": (247, 99, 12),
        "\N{MELON}": (228, 245, 119),
        "\N{PACKAGE}": (187, 145, 103),
        "\N{VIDEO CAMERA}": (200, 200, 200),
        "\N{NEWSPAPER}": (230, 230, 230),
        "\N{TICKET}": (105, 234, 255),
        "\N{BUSTS IN SILHOUETTE}": (117, 117, 117),
        "\N{KOALA}": (180, 180, 180),
        "\N{ONCOMING AUTOMOBILE}": (54, 148, 221),
        "\N{JACK-O-LANTERN}": (247, 99, 12),
        "\N{BRIEFCASE}": (142, 86, 46),
        "\N{NEW MOON WITH FACE}": (117, 117, 117),
        "\N{BASKETBALL AND HOOP}": (247, 99, 12),
        "\N{PIG FACE}": (238, 152, 137),
        "\N{WHITE HEAVY CHECK MARK}": (22, 198, 12),
        "\N{SQUARED CJK UNIFIED IDEOGRAPH-5272}": (234, 0, 94),
        "\N{SQUARED CJK UNIFIED IDEOGRAPH-7A7A}": (116, 77, 169),
        "\N{BROCCOLI}": (19, 161, 14),
        "\N{BANKNOTE WITH YEN SIGN}": (247, 218, 201),
        "\N{BANKNOTE WITH DOLLAR SIGN}": (248, 255, 179),
        "\N{BANKNOTE WITH EURO SIGN}": (220, 237, 189),
        "\N{BANKNOTE WITH POUND SIGN}": (213, 191, 253),
        "\N{SUNRISE OVER MOUNTAINS}": (174, 198, 46),
        "\N{BALL OF YARN}": (16, 122, 16),
        "\N{SPONGE}": (255, 200, 61),
        "\N{GRAPES}": (93, 47, 146),
        "\N{PEACH}": (247, 137, 74),
        "\N{POTATO}": (187, 145, 103),
        "\N{RADIO BUTTON}": (204, 204, 204),
        "\N{POTABLE WATER SYMBOL}": (0, 70, 255),
        "\N{YO-YO}": (154, 0, 137), "\N{BILLED CAP}": (0, 99, 177), "\N{FROG FACE}": (115, 170, 36)
    }

    img.resize((41, 45))
    arr = np.array(img)

    art = []
    has_alpha = bool(arr[0][0].shape[0] - 3)

    for row in arr:
        art_row = []

        for pixel in row:
            if has_alpha:
                alpha_mod = 255 - pixel[3]
                for index, value in enumerate(pixel):
                    pixel[index] = max(0, value - alpha_mod)

            min_colours = {}
            for name, mapped_rgb in colors.items():
                min_colours.update({sum((mapped_rgb[i] - pixel[i]) ** 2 for i in range(0, 3)): name})

            art_row.append(min_colours[min(min_colours)])
        art.append(art_row)

    return "\n".join("".join(art_row) for art_row in art)


