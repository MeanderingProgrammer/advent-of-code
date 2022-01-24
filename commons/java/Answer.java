package answer;

import lombok.experimental.UtilityClass;

@UtilityClass
public class Answer {

    public static void part1(int expected, int result) {
        part(1, expected, result);
    }

    public static void part2(int expected, int result) {
        part(2, expected, result);
    }

    private static void part(int part, int expected, int result) {
        if (expected != result) {
            throw new RuntimeException(String.format(
                "Part %d incorrect, expected %d but got %d", part, expected, result
            ));
        }
        System.out.printf("Part %d: %d \n", part, result);
    }
}
