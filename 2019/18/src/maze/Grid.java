package maze;

import java.util.*;

import lib.Point;
import lombok.*;
import lombok.experimental.FieldDefaults;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Grid {

    Map<Point, Node> grid;
    @Getter
    List<Point> keys;

    public Grid(List<String> maze) {
        this.grid = new HashMap<>();
        this.keys = new ArrayList<>();
        for (int y = 0; y < maze.size(); y++) {
            String row = maze.get(y);
            for (int x = 0; x < row.length(); x++) {
                char ch = row.charAt(x);
                if (ch != '#') {
                    var point = new Point(x, y);
                    var node = new Node(ch);
                    grid.put(point, node);
                    if (node.isKey()) {
                        this.keys.add(point);
                    }
                }
            }
        }

    }

    public Point getStart() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isStart())
                .map(Map.Entry::getKey)
                .findFirst()
                .orElseThrow(IllegalArgumentException::new);
    }

    public void remove(Point point) {
        this.grid.remove(point);
    }

    public Node get(Point point) {
        return grid.get(point);
    }

    public boolean contains(Point point) {
        return grid.containsKey(point);
    }
}
