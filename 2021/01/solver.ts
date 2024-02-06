import { Answer, Reader } from "aoc";

async function main(): Promise<void> {
  const values = await new Reader().read_int();
  Answer.part1(1292, window_increases(values, 1));
  Answer.part2(1262, window_increases(values, 3));
}

function window_increases(values: number[], window: number): number {
  let result = 0;
  for (let i = 0; i < values.length - window; i++) {
    if (window_sum(values, window, i + 1) > window_sum(values, window, i)) {
      result++;
    }
  }
  return result;
}

function window_sum(values: number[], window: number, start: number): number {
  return values
    .slice(start, start + window)
    .reduce((sum, value) => sum + value, 0);
}

await Answer.timer(main);
