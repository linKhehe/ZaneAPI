import io

import PIL

from .image_manager import ImageManager


class Pillow(ImageManager):

    @staticmethod
    def input(image_bytes) -> PIL.Image:
        return PIL.Image.open(io.BytesIO(image_bytes))

    @staticmethod
    def output(image_object) -> io.BytesIO:
        image_bytes = io.BytesIO()
        image_object.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        return image_bytes
