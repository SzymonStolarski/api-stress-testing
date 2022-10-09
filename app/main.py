from fastapi import FastAPI

from routers.auth import token
from routers.picture import invert
from routers.prime import check_prime
from routers.time import get


APP_VERSION = 'v1'


app = FastAPI()

app.include_router(token.router)
app.include_router(invert.router)
app.include_router(check_prime.router)
app.include_router(get.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.mount(f"/api/{APP_VERSION}", app)
