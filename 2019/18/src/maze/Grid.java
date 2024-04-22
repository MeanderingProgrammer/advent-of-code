package maze;

import java.util.*;

import lib.Position;
import lombok.*;
import lombok.experimental.FieldDefaults;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Grid {

    Map<Position, Node> grid;
    @Getter
    List<Position> keys;

    public Grid(List<String> maze) {
        this.grid = new HashMap<>();
        this.keys = new ArrayList<>();
        for (int y = 0; y < maze.size(); y++) {
            String row = maze.get(y);
            for (int x = 0; x < row.length(); x++) {
                char ch = row.charAt(x);
                if (ch != '#') {
                    var position = new Position(x, y);
                    var node = new Node(ch);
                    grid.put(position, node);
                    if (node.isKey()) {
                        this.keys.add(position);
                    }
                }
            }
        }

    }

    public Position getStart() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isStart())
                .map(Map.Entry::getKey)
                .findFirst()
                .orElseThrow(IllegalArgumentException::new);
    }

    public void remove(Position position) {
        this.grid.remove(position);
    }

    public Node get(Position position) {
        return grid.get(position);
    }

    public boolean contains(Position position) {
        return grid.containsKey(position);
    }
}
