package lib;

import java.util.Set;

public record Point(int x, int y) {

    public Point dx(int dx) {
        return new Point(x + dx, y);
    }

    public Point dy(int dy) {
        return new Point(x, y + dy);
    }

    public Set<Point> neighbors() {
        return Set.of(dx(1), dx(-1), dy(1), dy(-1));
    }
}
