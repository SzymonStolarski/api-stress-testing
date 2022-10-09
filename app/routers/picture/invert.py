import io

from fastapi import APIRouter, File, UploadFile
from PIL import Image, ImageOps


router = APIRouter()


class PillowInverter:

    def __init__(self):
        """Empty constructor"""
        pass

    def invert(self, img_data: bytes):
        img = Image.open(io.BytesIO(img_data))
        inverted_img = ImageOps.invert(img)

        return inverted_img


img_inverter = PillowInverter()


@router.post("/picture/invert/")
async def picture_invert(file: UploadFile = File(...)):

    img_data = await file.read()
    inverted_image = img_inverter.invert(img_data)

    return {'picture_name': file.filename}
