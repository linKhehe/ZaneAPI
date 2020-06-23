import io

import skimage.io
from wand.image import Image
import matplotlib.pyplot as plt


def bytes_to_wand(img_bytes: io.BytesIO):
    return Image(blob=img_bytes.getvalue())


def wand_to_bytes(img: Image):
    ret = io.BytesIO()
    img.save(ret)
    if img.format != "png":
        with Image(blob=ret.getvalue()) as converted:
            converted.format = "png"
            converted.save(ret)
    img.close()
    ret.seek(0)

    return ret


def bytes_to_np(img_bytes: io.BytesIO):
    ret = skimage.io.imread(img_bytes)
    return ret


def np_to_bytes(img_bytes: io.BytesIO):
    b = io.BytesIO()
    plt.imsave(b, img_bytes)
    b.seek(0)
    return b


def manipulation_numpy(func):
    def wrapper(image: io.BytesIO, *args, **kwargs):
        image = bytes_to_np(image)
        image = func(image, *args, **kwargs)
        return np_to_bytes(image)
    return wrapper


def manipulation_wand(func):
    def wrapper(image: io.BytesIO, *args, **kwargs):
        image = bytes_to_wand(image)
        image = func(image, *args, **kwargs)
        return wand_to_bytes(image)
    return wrapper
