import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch, clearToken } from "../api";
import type { Book } from "../types";

type Tab = "all" | "library";

function DashboardPage() {
  const navigate = useNavigate();
  const [tab, setTab] = useState<Tab>("all");
  const [books, setBooks] = useState<Book[]>([]);
  const [libraryBooks, setLibraryBooks] = useState<Book[]>([]);
  const [username, setUsername] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [pendingId, setPendingId] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError("");

      try {
        const query = search ? `?search=${encodeURIComponent(search)}` : "";
        const [booksResponse, libraryResponse, meResponse] = await Promise.all([
          apiFetch(`/books${query}`),
          apiFetch("/my-library"),
          apiFetch("/me"),
        ]);

        if (!booksResponse.ok || !libraryResponse.ok || !meResponse.ok) {
          throw new Error("Failed to load library data");
        }

        const booksData: { books: Book[] } = await booksResponse.json();
        const libraryData: { books: Book[] } = await libraryResponse.json();
        const meData: { id: number; username: string } = await meResponse.json();

        if (cancelled) {
          return;
        }

        setBooks(booksData.books);
        setLibraryBooks(libraryData.books);
        setUsername(meData.username);
      } catch (loadError) {
        if (cancelled) {
          return;
        }
        setError(
          loadError instanceof Error
            ? loadError.message
            : "Unable to load data.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [search]);

  const savedIds = new Set(libraryBooks.map((book) => book.id));

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSearch(searchInput.trim());
  }

  function handleLogout() {
    clearToken();
    localStorage.clear();
    navigate("/login");
  }

  async function handleSave(book: Book) {
    setPendingId(book.id);
    setError("");

    try {
      const response = await apiFetch(`/my-library/${book.id}`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error("Could not save book");
      }
      setLibraryBooks((current) =>
        current.some((saved) => saved.id === book.id)
          ? current
          : [...current, book],
      );
    } catch (saveError) {
      setError(
        saveError instanceof Error ? saveError.message : "Could not save book",
      );
    } finally {
      setPendingId(null);
    }
  }

  async function handleDelete(bookId: number) {
    setPendingId(bookId);
    setError("");

    try {
      const response = await apiFetch(`/my-library/${bookId}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Could not remove book");
      }
      setLibraryBooks((current) =>
        current.filter((book) => book.id !== bookId),
      );
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Could not remove book",
      );
    } finally {
      setPendingId(null);
    }
  }

  const visibleBooks = tab === "all" ? books : libraryBooks;

  return (
    <main className="page">
      <header className="topbar">
        <div>
          <h1>Library</h1>
          {username && <p className="muted">{username}</p>}
        </div>
        <button type="button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <div className="tabs">
        <button
          type="button"
          className={tab === "all" ? "is-active" : undefined}
          onClick={() => setTab("all")}
          aria-pressed={tab === "all"}
        >
          All Books
        </button>
        <button
          type="button"
          className={tab === "library" ? "is-active" : undefined}
          onClick={() => setTab("library")}
          aria-pressed={tab === "library"}
        >
          My Library
        </button>
      </div>

      {tab === "all" && (
        <form className="search-form" onSubmit={handleSearch}>
          <label className="sr-only" htmlFor="search">
            Search
          </label>
          <input
            id="search"
            type="search"
            placeholder="Search titles"
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      )}

      {error && (
        <p className="status alert" role="alert">
          {error}
        </p>
      )}
      {loading && <p className="status">Loading...</p>}

      {!loading && visibleBooks.length === 0 && (
        <p className="status muted">
          {tab === "all" ? "No books found." : "No books in your library yet."}
        </p>
      )}

      {!loading && (
        <ul className="book-list">
          {visibleBooks.map((book) => {
            const isSaved = savedIds.has(book.id);
            const isPending = pendingId === book.id;

            return (
              <li key={book.id} className="book-card">
                <img
                  className="book-cover"
                  src="/book-cover.jpg?v=2"
                  alt=""
                />
                <div className="book-info">
                  <span className="book-title">{book.title}</span>
                  <span className="book-author">{book.author ?? "Unknown author"}</span>
                  {tab === "all" ? (
                    isSaved ? (
                      <span className="saved" aria-label="Saved">
                        Saved ✓
                      </span>
                    ) : (
                      <button
                        type="button"
                        onClick={() => handleSave(book)}
                        disabled={isPending}
                        aria-label={`Save ${book.title}`}
                      >
                        {isPending ? "..." : "+ Save"}
                      </button>
                    )
                  ) : (
                    <button
                      className="danger"
                      type="button"
                      onClick={() => handleDelete(book.id)}
                      disabled={isPending}
                      aria-label={`Remove ${book.title}`}
                    >
                      {isPending ? "Removing..." : "Delete"}
                    </button>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </main>
  );
}

export default DashboardPage;
