const scores : number[] = [90, 75, 88]
const mixedArray : (number | string)[] = ["a", 1, "b", 2];

function average(nums: number[]) : number {
    if (nums.length === 0) {
        throw new Error("Cannot calculate average of an empty array.");
    }
    const total = nums.reduce((acc, num) => acc + num, 0);
    return total / nums.length;
}

const avgScore = average(scores);
console.log(`The average score is: ${avgScore}`);




