from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas import BookCreate, BookListResponse, BookRead
from database import Base, engine, get_db
import models  # This ensures that the Book model is registered with Base.metadata

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "Online"}

@app.get("/books", response_model=BookListResponse)
def get_books(search: str | None = None, session: Session = Depends(get_db)):
    statement = select(models.Book)
    if search:
        statement = statement.where(models.Book.title.ilike(f"%{search}%"))
    books = session.execute(statement).scalars().all()
    return {"books": books}

@app.post("/books", status_code=201, response_model=BookRead)
def create_book(book: BookCreate, session: Session = Depends(get_db)):
    new_book = models.Book(**book.model_dump())
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@app.get("/books/{id}", response_model=BookRead)
def get_book(id: int, session: Session = Depends(get_db)):
    book = session.get(models.Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book    