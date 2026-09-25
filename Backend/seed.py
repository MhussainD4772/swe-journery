import json

from sqlalchemy import func, select

from database import SessionLocal
from models import Book



def seed_data():
    db = SessionLocal()
    try: 
        # Do not seed if the database already has data
        existing_books = db.execute(select(func.count(Book.id))).scalar_one()
        if existing_books > 0:
            print("Database already seeded. Skipping seeding.")
            return

        # Load the JSON data from the file
        with open("books.json", "r") as file:
            data = json.load(file)

        # Add books to the session
        books = [Book(**book_data) for book_data in data]
        db.add_all(books)
        db.commit()
        print("Database seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()