function shout(input: unknown) : string {
    if (typeof input === "string") {
        return input.trim().toUpperCase();
    }
    throw new Error("Input must be a string");
}

console.log(shout("hello world"));
console.log(shout(42));

