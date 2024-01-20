package lib;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class AnswerTest {

    @Test
    void testSuccess() {
        Answer.part1(1, 1);
        Answer.part2("value", "value");
    }

    @Test
    void testFailure() {
        Assertions.assertThrows(RuntimeException.class, () -> Answer.part1(1, 2));
    }
}
