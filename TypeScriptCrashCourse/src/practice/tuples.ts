const user: [number, string, number, string] = [1, 'Mohd', 30, 'Engineer'];

function formatUser(person: [number, string, number, string]) : string {
    const [id, name, age, occupation] = person;
    return `User ID: ${id}, Name: ${name}, Age: ${age}, Occupation: ${occupation}`;
}

console.log(formatUser(user));
