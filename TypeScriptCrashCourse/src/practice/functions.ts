function greet(name: string, greeting: string = "Hello"): string {
    return `${greeting}, ${name}!`;
}

console.log(greet("Alice")); 
console.log(greet("Bob", "Hi"));   


function sum(...nums: number[]): number {
    return nums.reduce((acc, curr) => acc + curr, 0);
}

console.log(sum(1, 2, 3, 4)); 
console.log(sum(10, 20, 30));