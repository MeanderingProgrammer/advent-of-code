package lib;

import org.junit.jupiter.api.*;

class AnswerTest {

    @Test
    void testSuccess() {
        Answer.<Integer>part1(1, 1);
        Answer.<String>part2("value", "value");
    }

    @Test
    void testFailure() {
        Assertions.assertThrows(RuntimeException.class, () -> Answer.<Integer>part1(1, 2));
    }
}
