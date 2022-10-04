import io

from fastapi import FastAPI, File, UploadFile

from src.prime_number_checker.default_checker import DefaultChecker
from src.image_inverter.pillow_inverter import PillowInverter


app = FastAPI()

prime_checker = DefaultChecker()
img_inverter = PillowInverter()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/prime/{number}")
def prime(number: int):
    return {'result': prime_checker.check(number)}


@app.post("/picture/invert/")
async def picture_invert(file: UploadFile = File(...)):

    img_data = await file.read()
    inverted_image = img_inverter.invert(img_data)

    return {'picture_name': file.filename}
