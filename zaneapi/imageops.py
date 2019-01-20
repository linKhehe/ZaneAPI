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
    img.compression_quality = 1
    img.modulate(saturation=700)

    return img


def invert(img: Image):
    img.alpha_channel = False
    img.negate()

    return img


def desat(img: Image, threshold: int = 1):
    resize(img)
    img.modulate(saturation=100-(threshold*50))

    return img


def sat(img: Image, threshold: int = 1):
    resize(img)
    img.modulate(saturation=100+(threshold*50))

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
    img = img.fx("""iso=32; rone=rand(); rtwo=rand(); \
myn=sqrt(-2*ln(rone))*cos(2*Pi*rtwo); myntwo=sqrt(-2*ln(rtwo))* \
cos(2*Pi*rone); pnoise=sqrt(p)*myn*sqrt(iso)* \
channel(4.28,3.86,6.68,0)/255; max(0,p+pnoise)""")

    return img


def arc(img: Image):
    resize(img)
    img.virtual_pixel = "transparent"
    img.distort(method='arc', arguments=[360])

    return img


def concave(img: Image):
    resize(img)
    img.virtual_pixel = "transparent"
    img.background_color = Color("white")
    img.distort(method="barrel", arguments=[-.5, 0.0, 0.0, 1])

    return img


def convex(img: Image):
    resize(img)
    img.virtual_pixel = "transparent"
    img.background_color = Color("white")
    img.distort(method="barrel", arguments=[1, 0, 0, 1])

    return img


def floor(img: Image):
    resize(img, 128)
    img.alpha_channel = False
    img.background_color = Color("light-blue")
    img.virtual_pixel = "tile"

    img.distort(
        method="perspective",
        arguments=[
            0,
            0,
            20,
            61,

            90,
            0,
            70,
            63,

            0,
            90,
            0,
            83,

            90,
            90,
            85,
            88
        ]
    )

    resize(img, 512)

    return img


def blur(img: Image):
    resize(img)
    img.blur(0, 5)

    return img


def vaporwave(img: Image):
    resize(img)
    img.alpha_channel = False
    img.function('sinusoid', [3, -90, 0.2, 0.7])
    img.modulate(saturation=25, brightness=75)

    return img


def emboss(img: Image):
    resize(img)
    img.transform_colorspace('gray')
    img.emboss(radius=3, sigma=50)

    return img


def shade(img: Image):
    resize(img)
    img.shade(
        gray=True,
        azimuth=286.0,
        elevation=45.0
    )

    return img


def edge(img: Image):
    resize(img)
    img.alpha_channel = False
    img.transform_colorspace('gray')
    img.edge(2)

    return img


def bend(img: Image):
    resize(img)
    img.alpha_channel = False
    img.virtual_pixel = "transparent"
    img.distort(method="plane_2_cylinder", arguments=[90])

    return img


def posterize(img: Image):
    resize(img)
    img.posterize(2)

    return img


def grayscale(img: Image):
    resize(img)
    img.transform_colorspace('gray')

    return img
