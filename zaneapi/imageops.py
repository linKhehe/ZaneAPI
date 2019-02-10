import io
import asyncio
import functools
import numpy
import random
import math
import os

import colorsys
from wand.image import Image
from wand.color import Color
from PIL import Image as PILImage
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

loop = asyncio.get_event_loop()


class AsciiColor(Color):
    """
    A little subclass of wand.color.Color
    Adds functionality for ascii art.
    """

    def __init__(self, *args, **kwargs):
        self.ascii_characters = {
            300: "@",
            275: "#",
            250: ";",
            225: "+",
            200: "=",
            175: ":",
            150: "-",
            125: "\"",
            100: ",",
            75: "'",
            50: ".",
            25: " ",
            0: " "
        }
        super().__init__(*args, **kwargs)

    @property
    def ascii_character(self):
        value = self.red + self.green + self.blue
        value *= 100
        return self.ascii_characters[int(math.ceil(value / 25.) * 25)]


def resize(image: Image, max_size: int = 512):
    image.transform(resize=f'x{max_size}')
    image.transform(resize=f'{max_size}')


async def image_function(input_img: Image, func, *args):
    executor = functools.partial(func, input_img, *args)
    output_img = await loop.run_in_executor(None, executor)

    # assert isinstance(output_img, (Image, PILImage))

    if isinstance(output_img, str):
        return output_img

    b_io = io.BytesIO()

    if isinstance(output_img, Image):
        b_io_convert = io.BytesIO()
        if output_img.format == "jpeg":
            output_img.save(b_io_convert)
            with Image(blob=b_io_convert.getvalue()) as converted:
                converted.format = "png"
                output_img = converted
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


def shade(img: PILImage):
    # defining azimuth, elevation, and depth
    ele = numpy.pi / 2.2  # radians
    azi = numpy.pi / 4.  # radians
    dep = 10.  # (0-100)

    img = img.convert("L")
    # get an array
    a = numpy.asarray(img).astype('float')
    # find the gradient
    grad = numpy.gradient(a)
    # (it is two arrays: grad_x and grad_y)
    grad_x, grad_y = grad
    # getting the unit incident ray
    gd = numpy.cos(ele)  # length of projection of ray on ground plane
    dx = gd * numpy.cos(azi)
    dy = gd * numpy.sin(azi)
    dz = numpy.sin(ele)
    # adjusting the gradient by the "depth" factor
    # (I think this is how GIMP defines it)
    grad_x = grad_x * dep / 100.
    grad_y = grad_y * dep / 100.
    # finding the unit normal vectors for the image
    leng = numpy.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / leng
    uni_y = grad_y / leng
    uni_z = 1. / leng
    # take the dot product
    a2 = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
    # avoid overflow
    a2 = a2.clip(0, 255)
    # you must convert back to uint8 /before/ converting to an image
    img2 = PILImage.fromarray(a2.astype('uint8'))

    return img2


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


def lsd(img: Image):
    resize(img)
    img.alpha_channel = False
    img.function('sinusoid', [3, -90, 0.2, 0.7])
    img.modulate(saturation=200, brightness=75)

    return img


def sort(img: numpy.ndarray):
    img.sort(0)
    img.sort(1)

    img = PILImage.fromarray(img)

    return img


# def histogram(img: numpy.ndarray):
#     r = []
#     g = []
#     b = []
#
#     flat_img = img.flatten()
#
#     for px in range(0, flat_img.size, int(flat_img.size / 100)):
#         r.append(flat_img[px])
#     for px in range(1, flat_img.size, int(flat_img.size / 100)):
#         g.append(flat_img[px])
#     for px in range(2, flat_img.size, int(flat_img.size / 100)):
#         b.append(flat_img[px])
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     nbins = 20
#
#     for c, z, i in zip([r, g, b], [20, 10, 0], ["r", "g", "b"]):
#         hist, bins = numpy.histogram(c, bins=nbins)
#
#         colors = []
#         for c_i in range(0, 255, int(255 / 20)):
#             value = c_i / 255
#             if i == "r":
#                 colors.append([value, 0, 0, 1])
#             elif i == "g":
#                 colors.append([0, value, 0, 1])
#             elif i == "b":
#                 colors.append([0, 0, value, 1])
#
#         colors.sort()
#
#         xs = (bins[:-1] + bins[1:]) / 3
#
#         ax.bar(xs, hist, width=7, zs=z, zdir='y', color=colors, ec=colors, alpha=1)
#
#     plt.xlabel("Color Intensity")
#     ax.set_zlabel("Number of pixels.")
#
#     buff = io.BytesIO()
#     plt.savefig(buff, format='png')
#     plt.clf()
#     buff.seek(0)
#
#     img = PILImage.open(buff)
#
#     return img


def gay(img: Image):
    with Image(filename=f"{os.path.dirname(os.path.realpath(__file__))}\\api_assets\\gay.jpg") as gay:
        img.transform_colorspace("gray")
        img.transform_colorspace("rgb")
        gay.transparentize(.50)
        gay.sample(img.width, img.height)
        img.composite(gay, 0, 0)
    return img


def straight(img: Image):
    with Image(filename=f"{os.path.dirname(os.path.realpath(__file__))}\\api_assets\\straight.png") as straight:
        img.resize(640, 440)
        straight.composite(img, left=0, top=157)
        img = straight.clone()

    return img


def ascii_art(img: Image):
    with img:
        size = 200
        img.sample(size, int(size / 2))

        asciiart = ""

        first_iter = True
        for row in img:
            if not first_iter:
                asciiart += "\n"
            first_iter = False
            for col in row:
                with AsciiColor(str(col)) as c:
                    asciiart += c.ascii_character

    return asciiart
