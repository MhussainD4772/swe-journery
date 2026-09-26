from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from auth import create_access_token, get_current_user, hash_password, verify_password
from schemas import BookCreate, BookListResponse, BookRead, UserCreate, UserRead
from database import Base, engine, get_db
import models  # This ensures that the Book model is registered with Base.metadata

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/register", status_code=201, response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.username == user.username)
    existing_user = session.execute(statement).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.username == form_data.username)
    user = session.execute(statement).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

#Test endpoint
@app.get("/me", response_model=UserRead)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/my-library", response_model=BookListResponse)
def get_my_library(
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    statement = (
        select(models.Book)
        .join(models.SavedBook)
        .where(models.SavedBook.user_id == current_user.id)
    )
    books = session.execute(statement).scalars().all()
    return {"books": books}

@app.post("/my-library/{book_id}", status_code=201)
def save_book(
    book_id: int,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    book = session.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    already_saved = session.get(models.SavedBook, (current_user.id, book_id))
    if already_saved:
        return {"message": "Book already saved in your library"}
    session.add(models.SavedBook(user_id=current_user.id, book_id=book_id))
    session.commit()
    return {"message": "Book saved to your library"}

@app.delete("/my-library/{book_id}", status_code=204)
def remove_book(
    book_id: int,
    current_user: models.User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    saved_book = session.get(models.SavedBook, (current_user.id, book_id))
    if saved_book is None:
        raise HTTPException(status_code=404, detail="Book not found in your library")
    session.delete(saved_book)
    session.commit()
    return