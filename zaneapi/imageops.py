import io
import asyncio
import functools
from random import shuffle

import colorsys
from wand.image import Image
from PIL import Image as PILImage

loop = asyncio.get_event_loop()


def resize(image: Img, max_size: int = 512):
    if image.width > max_size:
        image.transform(f"{max_size}")
    elif image.height > max_size:
        image.transform(f"x{max_size}")
    return image
        
    
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
    with img:
        resize(img)
        img.negate()
    
        # this shouldn't be necessary but this is returning
        # blank images so I am gonna make a new image from 
        # the inverted one and try that
    
        output_img = Image(img)
    
    return output_img


def desat(img: PILImage, threshold: int = 2):
    img_new = PILImage.new("RGBA", img.size)
    _x, _y = img.size
    for x in range(_x):
        for y in range(_y):
            px = img.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(*px[:3])
            s /= threshold
            img_new.putpixel((x, y), tuple(map(int, colorsys.hsv_to_rgb(h, s, v))))
    return img_new


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


def noise(img: PILImage):
    _x, _y = img.size
    img_new = PILImage.new("RGBA", img.size)
    for x in range(_x):
        for y in range(_y):
            px = img.getpixel((x, y))
            _px = list(px[:3])
            shuffle(_px)
            img_new.putpixel((x, y), tuple(_px))
    return img_new
