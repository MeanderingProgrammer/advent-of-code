package lib;

import lombok.experimental.UtilityClass;

@UtilityClass
public class Answer {

  public void timer(Runnable solution) {
    long start = System.nanoTime();
    solution.run();
    long end = System.nanoTime();
    System.out.printf("Runtime (ns): %d\n", end - start);
  }

  public <T> void part1(T expected, T result) {
    part(1, expected, result);
  }

  public <T> void part2(T expected, T result) {
    part(2, expected, result);
  }

  private <T> void part(int part, T expected, T result) {
    if (!expected.equals(result)) {
      var errorFormat = "Part %d incorrect, expected %s but got %s";
      throw new RuntimeException(String.format(errorFormat, part, expected, result));
    }
    System.out.printf("Part %d: %s\n", part, result);
  }
}
