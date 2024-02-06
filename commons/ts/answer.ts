export class Answer {
  static async timer(solution: () => Promise<void>): Promise<void> {
    const start = Bun.nanoseconds();
    await solution();
    const end = Bun.nanoseconds();
    console.log(`Runtime (ns): ${end - start}`);
  }

  static part1(expected: number, result: number): void {
    Answer.part(1, expected, result);
  }

  static part2(expected: number, result: number): void {
    Answer.part(2, expected, result);
  }

  private static part(part: number, expected: number, result: number): void {
    if (expected != result) {
      throw new Error(
        `Part ${part} incorrect, expected ${expected} but got ${result}`,
      );
    } else {
      console.log(`Part ${part}: ${result}`);
    }
  }
}
