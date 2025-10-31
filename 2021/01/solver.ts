import { Answer, Reader } from "aoc";

async function main(): Promise<void> {
  const values = await new Reader().intLines();
  Answer.part1(1292, windowIncreases(values, 1));
  Answer.part2(1262, windowIncreases(values, 3));
}

function windowIncreases(values: number[], window: number): number {
  let result = 0;
  for (let i = 0; i < values.length - window; i++) {
    if (windowSum(values, window, i + 1) > windowSum(values, window, i)) {
      result++;
    }
  }
  return result;
}

function windowSum(values: number[], window: number, start: number): number {
  return values
    .slice(start, start + window)
    .reduce((sum, value) => sum + value, 0);
}

await Answer.timer(main);
