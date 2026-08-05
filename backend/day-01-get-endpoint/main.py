from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Health(BaseModel):
    status: str
    version: str


@app.get("/Health", response_model=Health)
def health():
    return Health(status="ok", version="1.0.0")
