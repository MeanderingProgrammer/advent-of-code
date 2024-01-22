package maze;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import lib.Position;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Grid {

    Map<Position, Node> grid;
    @Getter
    List<Position> keys;
    @Getter
    Position start;

    public Grid(List<String> maze, Position start) {
        this.grid = initializeGrid(maze);
        this.keys = computeKeys();
        this.start = Optional.ofNullable(start).orElseGet(this::computeStart);
    }

    public Grid(List<String> maze) {
        this(maze, null);
    }

    public Node get(Position position) {
        return grid.get(position);
    }

    public boolean contains(Position position) {
        return grid.containsKey(position);
    }

    public int totalKeys() {
        return keys.size();
    }

    private static Map<Position, Node> initializeGrid(List<String> maze) {
        Map<Position, Node> grid = new HashMap<>();
        for (int y = 0; y < maze.size(); y++) {
            String row = maze.get(y);
            for (int x = 0; x < row.length(); x++) {
                char ch = row.charAt(x);
                if (ch != '#') {
                    grid.put(new Position(x, y), new Node(ch));
                }
            }
        }
        return grid;
    }

    private List<Position> computeKeys() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isKey())
                .map(Map.Entry::getKey)
                .toList();
    }

    private Position computeStart() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isStart())
                .map(Map.Entry::getKey)
                .findFirst()
                .orElseThrow(IllegalArgumentException::new);
    }
}
