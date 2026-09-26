import { useEffect, useState, type FormEvent } from "react";
import type {Book} from "./types";
import {BookCard} from "./BookCard";

function App() {
    const [books, setBooks] = useState<Book[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");

    useEffect(() => {
        const controller = new AbortController();

        const fetchBooks = async () => {
            try {
                const response = await fetch(
                    "https://jsonplaceholder.typicode.com/posts?_limit=5",
                    { signal: controller.signal }
                );
                if (!response.ok) {
                    throw new Error(`Request failed with status ${response.status}`);
                }

                const posts: { id: number; title: string; body: string }[] = await response.json();
                setBooks(posts.map((post) => ({
                    id: post.id,
                    title: post.title,
                    author: post.body,
                    published: true
                })));
            } catch (fetchError) {
                if (!controller.signal.aborted) {
                    setError(fetchError instanceof Error ? fetchError.message : "Failed to fetch books.");
                }
            } finally {
                if (!controller.signal.aborted) {
                    setLoading(false);
                }
            }
        };

        void fetchBooks();
        return () => controller.abort();
    }, []);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const trimmedTitle = title.trim();
        const trimmedAuthor = author.trim();
        if (!trimmedTitle || !trimmedAuthor) return;

        setBooks((currentBooks) => [
            ...currentBooks,
            {
                id: Math.max(0, ...currentBooks.map((book) => book.id)) + 1,
                title: trimmedTitle,
                author: trimmedAuthor,
                published: false
            }
        ]);
        setTitle("");
        setAuthor("");
    };

    const handleDelete = (bookId: number) => {
        setBooks((currentBooks) => currentBooks.filter((book) => book.id !== bookId));
    };

    const filteredBooks = books.filter((book) =>
        book.title.toLowerCase().includes(searchTerm.trim().toLowerCase())
    );

    return(
        <div>
        <h1>My Book App</h1>
        <button onClick={() => setBooks([])}>Clear</button>
        <label>
            Search books
            <input
                type="search"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
            />
        </label>
        <form onSubmit={handleSubmit}>
            <label>
                Title
                <input
                    required
                    value={title}
                    onChange={(event) => setTitle(event.target.value)}
                />
            </label>
            <label>
                Author
                <input
                    required
                    value={author}
                    onChange={(event) => setAuthor(event.target.value)}
                />
            </label>
            <button type="submit">Add book</button>
        </form>
        {loading ? (
            <p>Loading...</p>
        ) : error ? (
            <p>{error}</p>
        ) : books.length === 0 ? (
            <p>No books yet</p>
        ) : filteredBooks.length === 0 ? (
            <p>No books match your search.</p>
        ) : (
            filteredBooks.map((book) => (
                <BookCard
                    key={book.id}
                    book={book}
                    onDelete={handleDelete}
                />
            ))
        )}
        </div>
    );
};

export default App;