import io

from PIL import Image, ImageOps

from src.image_inverter.base_inverter import BaseImageInverter


class PillowInverter(BaseImageInverter):

    def __init__(self):
        super().__init__()

    def invert(self, img_data: bytes):
        img = Image.open(io.BytesIO(img_data))
        inverted_img = ImageOps.invert(img)

        return inverted_img
