import type { Book } from "./types";

interface BookCardProps {
  book: Book;
  onDelete: (bookId: number) => void;
}

export function BookCard({ book, onDelete }: BookCardProps) {
  return (
    <article>
      <h2>{book.title}</h2>
      <p>{book.author}</p>
      <p>{book.published ? "Published" : "Not published"}</p>
      {book.rating !== undefined && <p>Rating: {book.rating}</p>}
      <button onClick={() => onDelete(book.id)}>Delete</button>
    </article>
  );
}
