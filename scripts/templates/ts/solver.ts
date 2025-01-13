import { Answer, Reader } from "aoc";

async function main(): Promise<void> {
  const data = await new Reader().read();
  console.log(data);
  Answer.part1(1, 1);
  Answer.part2(1, 1);
}

await Answer.timer(main);
