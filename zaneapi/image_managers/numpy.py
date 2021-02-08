import io

import numpy as np
import PIL
from matplotlib import pyplot as plt

from .image_manager import ImageManager


class Numpy(ImageManager):

    @staticmethod
    def input(image_bytes) -> np.ndarray:
        image = PIL.Image.open(io.BytesIO(image_bytes))
        return np.array(image)

    @staticmethod
    def output(arr) -> io.BytesIO:
        image_bytes = io.BytesIO()
        plt.imsave(image_bytes, arr)
        image_bytes.seek(0)
        return image_bytes
