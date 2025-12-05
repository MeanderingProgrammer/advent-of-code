import { Answer, Reader } from "aoc";

async function main(): Promise<void> {
  const values = await new Reader().intLines();
  Answer.part1(1292, increases(values, 1));
  Answer.part2(1262, increases(values, 3));
}

function increases(values: number[], n: number): number {
  let result = 0;
  for (let i = 0; i < values.length - n; i++) {
    if (sum(values, n, i + 1) > sum(values, n, i)) {
      result++;
    }
  }
  return result;
}

function sum(values: number[], n: number, start: number): number {
  return values.slice(start, start + n).reduce((sum, value) => sum + value, 0);
}

await Answer.timer(main);
