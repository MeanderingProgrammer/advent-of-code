package lib;

import java.util.Set;

import org.junit.jupiter.api.*;

class PointTest {

    @Test
    void testNeighbors() {
        var point = new Point(-1, 3);
        Assertions.assertEquals(-1, point.x());
        Assertions.assertEquals(3, point.y());
        var expected = Set.of(new Point(-1, 2), new Point(-1, 4), new Point(0, 3), new Point(-2, 3));
        Assertions.assertEquals(expected, point.neighbors());
    }

    @Test
    void testDxDy() {
        var point = new Point(-1, 3);
        Assertions.assertEquals(new Point(-2, 3), point.dx(-1));
        Assertions.assertEquals(new Point(-1, 7), point.dy(4));
    }
}
