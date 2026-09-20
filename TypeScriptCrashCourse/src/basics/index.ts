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