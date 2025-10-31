export class Answer {
  static async timer(solution: () => Promise<void>): Promise<void> {
    const start = Bun.nanoseconds();
    await solution();
    const end = Bun.nanoseconds();
    console.log(`Runtime (ns): ${end - start}`);
  }

  static part1<T>(expected: T, actual: T): void {
    Answer.part(1, expected, actual);
  }

  static part2<T>(expected: T, actual: T): void {
    Answer.part(2, expected, actual);
  }

  private static part<T>(part: number, expected: T, actual: T): void {
    if (expected != actual) {
      throw new Error(
        `Part ${part} incorrect, expected ${expected} but got ${actual}`,
      );
    } else {
      console.log(`Part ${part}: ${actual}`);
    }
  }
}
