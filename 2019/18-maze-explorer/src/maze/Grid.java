package maze;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import pojo.Position;

public class Grid {

    private final Map<Position, Node> grid;
    private final List<Position> keyPositions;
    private final Position startingPosition;

    public Grid(List<String> maze, Position startingPosition) {
        grid = initializeGrid(maze);
        keyPositions = computeKeyPositions();
        if (startingPosition == null) {
            this.startingPosition = computeStartingPosition();
        } else {
            this.startingPosition = startingPosition;
        }
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

    public List<Position> getKeyPositions() {
        return keyPositions;
    }

    public int totalKeys() {
        return keyPositions.size();
    }

    public Position getStartingPosition() {
        return startingPosition;
    }

    @Override
    public String toString() {
        return grid.entrySet().stream()
                .map(entry -> String.format("%s = %s", entry.getKey(), entry.getValue()))
                .collect(Collectors.joining("\n"));
    }

    private static Map<Position, Node> initializeGrid(List<String> maze) {
        Map<Position, Node> grid = new HashMap<>();
        for (int y = 0; y < maze.size(); y++) {
            String row = maze.get(y);
            for (int x = 0; x < row.length(); x++) {
                Position position = new Position(x, y);
                grid.put(position, new Node(row.charAt(x)));
            }
        }
        return grid;
    }

    private List<Position> computeKeyPositions() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isKey())
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }

    private Position computeStartingPosition() {
        return grid.entrySet().stream()
                .filter(entry -> entry.getValue().isStartingPoint())
                .map(Map.Entry::getKey)
                .findFirst()
                .orElseThrow(IllegalArgumentException::new);
    }
}
