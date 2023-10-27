package maze;

import java.util.*;
import lib.Position;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Grid {

  private static final char WALL = '#';

  Map<Position, Node> grid;
  @Getter List<Position> keyPositions;
  @Getter Position startingPosition;

  public Grid(List<String> maze, Position startingPosition) {
    this.grid = initializeGrid(maze);
    this.keyPositions = computeKeyPositions();
    this.startingPosition =
        Optional.ofNullable(startingPosition).orElseGet(this::computeStartingPosition);
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
    return keyPositions.size();
  }

  private static Map<Position, Node> initializeGrid(List<String> maze) {
    Map<Position, Node> grid = new HashMap<>();
    for (int y = 0; y < maze.size(); y++) {
      String row = maze.get(y);
      for (int x = 0; x < row.length(); x++) {
        char ch = row.charAt(x);
        if (ch != WALL) {
          grid.put(new Position(x, y), new Node(ch));
        }
      }
    }
    return grid;
  }

  private List<Position> computeKeyPositions() {
    return grid.entrySet().stream()
        .filter(entry -> entry.getValue().isKey())
        .map(Map.Entry::getKey)
        .toList();
  }

  private Position computeStartingPosition() {
    return grid.entrySet().stream()
        .filter(entry -> entry.getValue().isStartingPoint())
        .map(Map.Entry::getKey)
        .findFirst()
        .orElseThrow(IllegalArgumentException::new);
  }
}
