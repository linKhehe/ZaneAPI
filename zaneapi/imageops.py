import io
import asyncio
import functools

from wand.image import Image

loop = asyncio.get_event_loop()


def resize(img: Image, width: int):
    if img.width < width and img.height < width:
        aspect = img.width / img.height
        img.sample(width=int(width), height=int(width * aspect))
    return img


async def image_function(input_img: Image, func, *args):
    executor = functools.partial(func, input_img, *args)
    output_img = await loop.run_in_executor(None, executor)

    assert isinstance(output_img, Image)

    b_io = io.BytesIO()
    output_img.save(b_io)
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
    resize(img, 512)

    img.format = "jpeg"
    img.compression_quality = 2
    img.modulate(saturation=700)

    return img


def invert(img: Image):
    resize(img, 1920)
    img.negate()

    return img
