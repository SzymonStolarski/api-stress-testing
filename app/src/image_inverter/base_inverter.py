from abc import ABC, abstractmethod


class BaseImageInverter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def invert(self, img_data: bytes):
        pass
