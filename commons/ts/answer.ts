export class Answer {
  static async timer(solution: () => Promise<void>): Promise<void> {
    const start = Bun.nanoseconds();
    await solution();
    const end = Bun.nanoseconds();
    console.log(`Runtime (ns): ${end - start}`);
  }

  static part1(expected: number, actual: number): void {
    Answer.part(1, expected, actual);
  }

  static part2(expected: number, actual: number): void {
    Answer.part(2, expected, actual);
  }

  private static part(part: number, expected: number, actual: number): void {
    if (expected != actual) {
      throw new Error(
        `Part ${part} incorrect, expected ${expected} but got ${actual}`,
      );
    } else {
      console.log(`Part ${part}: ${actual}`);
    }
  }
}
