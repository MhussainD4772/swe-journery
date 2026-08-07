from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LogEntry(BaseModel):
    id: int
    message: str

logs = [
    LogEntry(id=1, message="What even is fastapi"),
    LogEntry(id=2, message="What even is python"),
    LogEntry(id=3, message="What even is life"),
]


@app.get("/logs")
def get_logs(limit: int = 10) -> list[LogEntry]:
    return(logs[:limit])


@app.get("/logs/{logs_id}")
def read_logs(logs_id: int):
    for log in logs:
        if log.id == logs_id:
            return log





































