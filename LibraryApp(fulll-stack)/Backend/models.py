from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import ForeignKey


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str | None] = mapped_column()
    description: Mapped[str | None] = mapped_column()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

class SavedBook(Base):
    __tablename__ = "saved_books"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)