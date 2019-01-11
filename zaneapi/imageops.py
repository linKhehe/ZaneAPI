import io
import asyncio
import functools
import uuid


from wand.image import Image

loop = asyncio.get_event_loop()


async def save_image(img: Image):
    unique_uuid = str(uuid.uuid4())
    file = f"C:\\Users\\Liam\\PycharmProjects\\Meme-Imaging\\ZaneAPI\\zaneapi\\tmp\\{unique_uuid}"
    img.format = "png"
    img.save(filename=file)

    return unique_uuid


async def image_function(input_img: Image, func, *args):
    executor = functools.partial(func, input_img, *args)
    output_img = await loop.run_in_executor(None, executor)

    assert isinstance(output_img, Image)

    b_io = io.BytesIO()
    output_img.save(b_io)
    b_io.seek(0)

    return b_io


def magic(img: Image):
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
    img.sample(512, 512)

    return img


def deepfry(img: Image):
    img.format = "jpeg"
    img.compression_quality = 2
    img.modulate(saturation=700)
    img.sample(512, 512)
    img.format = "png"

    return img
