package lib;

import java.util.Set;

public record Position(int x, int y) {

    public Position dx(int dx) {
        return new Position(x + dx, y);
    }

    public Position dy(int dy) {
        return new Position(x, y + dy);
    }

    public Set<Position> adjacent() {
        return Set.of(dx(1), dx(-1), dy(1), dy(-1));
    }
}
