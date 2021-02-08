import io

import wand
import wand.image

from .image_manager import ImageManager


class Wand(ImageManager):

    @staticmethod
    def input(image_bytes) -> wand.image.Image:
        return wand.image.Image(blob=image_bytes)

    @staticmethod
    def output(image_object) -> io.BytesIO:
        image_bytes = io.BytesIO()
        image_object.save(image_bytes)
        image_bytes.seek(0)
        return image_bytes
