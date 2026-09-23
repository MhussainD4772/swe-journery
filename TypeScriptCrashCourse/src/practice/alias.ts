type ID = number | string;

function printId(id: ID): void {
    if (typeof id === "string") {
        console.log(id.toUpperCase());
    } else {
        console.log(id);
    } 
}

const myId: ID = 123;
printId(myId); // Output: 123

const anotherId: ID = "abc";
printId(anotherId); // Output: ABC


type Point = {readonly x: number; readonly y: number};

function printPoint(point: Point): void {
    console.log(`x: ${point.x}, y: ${point.y}`);
}
const myPoint: Point = { x: 10, y: 20 };
printPoint(myPoint);
