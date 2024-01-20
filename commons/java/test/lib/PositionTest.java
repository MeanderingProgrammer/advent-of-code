package lib;

import java.util.*;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class PositionTest {

    @Test
    void testAdjacent() {
        var position = new Position(-1, 3);
        Assertions.assertEquals(-1, position.x());
        Assertions.assertEquals(3, position.y());
        Assertions.assertEquals(
            Set.of(new Position(-1, 2), new Position(-1, 4), new Position(0, 3), new Position(-2, 3)), 
            position.adjacent()
        );
    }
}
