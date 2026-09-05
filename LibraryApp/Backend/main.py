from fastapi import FastAPI

from database import Base, engine
import models  # This ensures that the Book model is registered with Base.metadata

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "Sab set hai mama"}
