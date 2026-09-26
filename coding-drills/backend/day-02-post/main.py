from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LogEntry(BaseModel):
    message: str

@app.post("/logs")
def create_log(entry: LogEntry):
    return{"received", entry.message}

