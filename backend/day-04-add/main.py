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

class LogCreate(BaseModel):
    message: str


logs = [
    LogEntry(id=1, message="Why is fastapi the best"),
    LogEntry(id=2, message="What are the advantages of writing code by hand in the age of AI"),
    LogEntry(id=3, message="How to get better at Fullstack development"),
]

@app.get("/logs")
def get_logs(limit: int = 3) -> list[LogEntry]:
    return(logs[:limit])

@app.post("/logs")
def create_log(entry: LogCreate):
    new_id = len(logs) + 1
    new_log = LogEntry(id=new_id, message=entry.message)
    logs.append(new_log)
    return new_log









