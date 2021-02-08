import abc


class ImageManager(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def input(image_bytes):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def output(image_object):
        raise NotImplementedError
