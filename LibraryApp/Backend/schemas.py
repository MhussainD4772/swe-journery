from pydantic import BaseModel, ConfigDict


class BaseBook(BaseModel):
    title: str
    author: str | None = None
    description: str | None = None


class BookCreate(BaseBook):
    pass

class BookRead(BaseBook):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookListResponse(BaseModel):
    books: list[BookRead]

    
