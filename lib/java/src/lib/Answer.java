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

    public <T> void part1(T expected, T actual) {
        part(1, expected, actual);
    }

    public <T> void part2(T expected, T actual) {
        part(2, expected, actual);
    }

    private <T> void part(int part, T expected, T actual) {
        if (!expected.equals(actual)) {
            var errorFormat = "Part %d: expected %s got %s";
            throw new RuntimeException(String.format(errorFormat, part, expected, actual));
        }
        System.out.printf("Part %d: %s\n", part, actual);
    }
}
