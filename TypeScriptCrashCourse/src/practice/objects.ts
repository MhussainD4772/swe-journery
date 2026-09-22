interface Book {
    id: number;
    title: string;
    author: string;
    published: boolean;
    rating?: number; // Optional property
} 

function describeBook(book: Book) : string {
    const  { id, title, author, published, rating } = book;
    let result = `Book ID: ${id}\nTitle: ${title}\nAuthor: ${author}\nPublished: ${published ? "Yes" : "No"}`;
    if (rating !== undefined) {
        result += `\nRating: ${rating}`;
    }
    return result;
}

console.log(describeBook({ id: 1, title: "TypeScript Basics", author: "John Doe", published: true}));
console.log(describeBook({ id: 2, title: "Advanced TypeScript", author: "Jane Smith", published: false, rating: 4.0 }));