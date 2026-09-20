let sales = 109_098_898
let course = 'TypeScript'
let is_published = true
console.log(sales)
console.log(course)
console.log(is_published)

function render(document: any) {
    console.log(document)
}
render('Hello, TypeScript!')


let numbers: number[] = [1, 2, 3]
let numbers2: Array<number> = [1, 2, 3]
console.log(numbers)
console.log(numbers2)

let numberss: number[] = []
console.log(numberss)


let user: [number, string] = [1, 'MD']
console.log(user);


function calculateTax(number: number, taxYear: number): number{
    return number * 0.2
}
console.log(calculateTax(10, 2020));
console.log(calculateTax(10, 2020));


let employee: {readonly id: number, name: string} = {id: 1, name: 'MD'};
console.log(employee);
