from datetime import datetime, timedelta

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import src.authentication.authentication as ath
from src.authentication.hour import get_current_time
from src.image_inverter.pillow_inverter import PillowInverter
from src.prime_number_checker.default_checker import DefaultChecker


app = FastAPI()

prime_checker = DefaultChecker()
img_inverter = PillowInverter()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/prime/{number}")
def prime(number: int):

    try:
        return {'result': prime_checker.check(number)}
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Wrong number passed!"
        )


@app.post("/picture/invert/")
async def picture_invert(file: UploadFile = File(...)):

    img_data = await file.read()
    inverted_image = img_inverter.invert(img_data)

    return {'picture_name': file.filename}


@app.post("/token", response_model=ath.Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = ath.authenticate_user(
        ath.fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ath.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = ath.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/time")
def current_time(time: datetime = Depends(get_current_time)):
    return time
