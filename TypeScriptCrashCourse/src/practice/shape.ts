type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; size: number };
type Rectangle = { kind: "rectangle"; width: number; height: number };
type Triangle = { kind: "triangle"; base: number; height: number };

type Shape = Circle | Square | Rectangle | Triangle;

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.size ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      const _exhaustiveCheck: never = shape;
        throw new Error(`Unhandled shape kind: ${_exhaustiveCheck}`);
  }
}   


console.log(area({ kind: "circle", radius: 5 })); // Output: 78.53981633974483
console.log(area({ kind: "square", size: 4 })); // Output: 16
console.log(area({ kind: "rectangle", width: 3, height: 6 }));
console.log(area({ kind: "triangle", base: 4, height: 5 })); // Output: 10
