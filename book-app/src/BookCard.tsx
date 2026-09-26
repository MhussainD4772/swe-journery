import type Book from "./types";

interface BookCardProps {
  book: Book;
}

export function BookCard({ book }: BookCardProps) {
  return <div>{book.title}</div>;
}
