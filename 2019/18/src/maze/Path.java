package maze;

import java.util.*;

import lib.Point;

public record Path(Point key, char value, Set<Character> needed, int distance) {
    public Path addKey(char ch) {
        var updated = new HashSet<>(this.needed);
        updated.add(ch);
        return new Path(this.key, this.value, updated, this.distance);
    }

    public Path next() {
        return new Path(this.key, this.value, this.needed, this.distance + 1);
    }
}
