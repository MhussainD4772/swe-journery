from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LogEntry(BaseModel):
    id: int
    message: str


logs = [
    LogEntry(id=1, message="This is my first challenge"),
    LogEntry(id=2, message="Winners do not quite"),
    LogEntry(id=3, message="Todays is a chest day"),
]


@app.get("/logs")
def get_logs(limit: int = 10) -> list[LogEntry]:
    return (logs[:limit])

@app.get("/logs/{logs_id}")
def read_id(logs_id: int):
    for log in logs:
        if log.id == logs_id:
            return log

