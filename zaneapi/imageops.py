import io
import asyncio
import functools

import colorsys
from wand.image import Image
from wand.color import Color
from PIL import Image as PILImage

loop = asyncio.get_event_loop()


def resize(image: Image, max_size: int = 512):
    image.transform(resize=f'x{max_size}')
    image.transform(resize=f'{max_size}')


async def image_function(input_img: Image, func, *args):
    executor = functools.partial(func, input_img, *args)
    output_img = await loop.run_in_executor(None, executor)

    # assert isinstance(output_img, (Image, PILImage))

    b_io = io.BytesIO()
    if isinstance(output_img, Image):
        output_img.format = "png"
        output_img.save(b_io)
    else:
        output_img.save(b_io, "png")
    b_io.seek(0)

    return b_io


def magic(img: Image):
    resize(img, 256)
    img.liquid_rescale(
        width=int(img.width * 0.5),
        height=int(img.height * 0.5),
        delta_x=1,
        rigidity=0
    )
    img.liquid_rescale(
        width=int(img.width * 1.5),
        height=int(img.height * 1.5),
        delta_x=2,
        rigidity=0
    )

    return img


def deepfry(img: Image):
    resize(img)
    img.format = "jpeg"
    img.compression_quality = 2
    img.modulate(saturation=700)

    return img


def invert(img: Image):
    img.alpha_channel = False
    img.negate()

    return img


def desat(img: Image, threshold: int = 2):
    resize(img)
    img.modulate(saturation=100-(threshold*15))

    return img


def colormap(img: PILImage, color: tuple):
    bh, _, _ = colorsys.rgb_to_hsv(*color)
    _x, _y = img.size
    img_new = PILImage.new("RGBA", img.size)
    for x in range(_x):
        for y in range(_y):
            px = img.getpixel((x, y))
            _, s, v = colorsys.rgb_to_hsv(*px[:3])
            r, g, b = colorsys.hsv_to_rgb(bh, s, v)
            img_new.putpixel((x, y), tuple(map(int, (r, g, b))))
    return img_new


def noise(img: Image):
    resize(img, 256)
    img.evaluate()

    return img


def arc(img: Image):
    resize(img)
    img.distort(method='arc', arguments=[360])

    return img


def concave(img: Image):
    resize(img)
    img.background_color = Color("white")
    img.distort(method="barrel", arguments=[-0.2, 0.0, 0.0, 1.3])

    return img


def convex(img: Image):
    resize(img)
    img.background_color = Color("white")
    img.distort(method="barrel", arguments=[0.2, 0.0, 0.0, 1.0])

    return img
