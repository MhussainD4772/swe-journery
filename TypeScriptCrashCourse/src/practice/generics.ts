function last<T>(items: T[]): T | undefined {
    return items[items.length - 1];
}

function wrapInArray<T>(item: T): T[] {
    return [item];
}

// Example usage:
const wrappedNumber = wrapInArray(42); // wrappedNumber is of type number[] and equals [42]
const wrappedString = wrapInArray('hello'); // wrappedString is of type string[] and equals ['hello']


// Example usage:
const numbers = [1, 2, 3, 4, 5];
const lastNumber = last(numbers); // lastNumber is of type number and equals 5

const strings = ['a', 'b', 'c'];
const lastString = last(strings); // lastString is of type string and equals 'c'

console.log(wrappedNumber); // Output: [42]
console.log(wrappedString);
console.log(lastNumber); // Output: 5
console.log(lastString); // Output: 'c'