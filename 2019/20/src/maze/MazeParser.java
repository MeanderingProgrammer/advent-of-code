package maze;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import lib.Position;
import lombok.AccessLevel;
import lombok.experimental.FieldDefaults;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class MazeParser {

  private static final Set<Character> MAZE_CHARACTERS = Set.of('#', '.');
  private static final Set<Character> NON_LABEL_CHARACTERS = Set.of('#', '.', ' ');

  List<String> maze;
  int mazeSize;

  public MazeParser(List<String> maze) {
    this.maze = maze;

    String middleRow = maze.get(maze.size() / 2);
    int mazeCharacters =
        (int) middleRow.chars().mapToObj(ch -> (char) ch).filter(MAZE_CHARACTERS::contains).count();
    this.mazeSize = mazeCharacters / 2;
  }

  public Map<Node, Set<Edge>> asGraph() {
    Map<Position, Node> nodes = getNodes();
    return nodes.entrySet().stream()
        .collect(Collectors.toMap(Map.Entry::getValue, entry -> getEdges(entry.getKey(), nodes)));
  }

  private Map<Position, Node> getNodes() {
    Map<Position, Node> nodes = new HashMap<>();
    for (int r = 0; r < maze.size(); r++) {
      int row = r;
      nodes.putAll(getNodes(maze.get(r), c -> new Position(c, row)));
    }
    for (int c = 0; c < maze.get(0).length(); c++) {
      int column = c;
      nodes.putAll(getNodes(getColumn(c), r -> new Position(column, r)));
    }
    return nodes;
  }

  private Map<Position, Node> getNodes(String rowColumn, Function<Integer, Position> creator) {
    Map<Position, Node> nodes = new HashMap<>();
    for (var startIndex : getStartIndices(rowColumn)) {
      var label = startIndex.getLabel(rowColumn);
      if (label.isPresent()) {
        var position = creator.apply(startIndex.getPositionIndex());
        nodes.put(position, new Node(label.get(), startIndex.inner()));
      }
    }
    return nodes;
  }

  private Set<NodeStart> getStartIndices(String rowColumn) {
    return Set.of(
        new NodeStart(0, true, false),
        new NodeStart(mazeSize + 2, false, true),
        new NodeStart(rowColumn.length() - mazeSize - 4, true, true),
        new NodeStart(rowColumn.length() - 2, false, false));
  }

  private String getColumn(int column) {
    StringBuilder result = new StringBuilder();
    for (String row : maze) {
      result.append(row.charAt(column));
    }
    return result.toString();
  }

  private Set<Edge> getEdges(Position position, Map<Position, Node> nodes) {
    Position mazePosition =
        position.adjacent().stream()
            .filter(this::inMaze)
            .findFirst()
            .orElseThrow(() -> new RuntimeException("Couldn't find maze entrance"));
    return getEdges(mazePosition, nodes, new HashSet<>(List.of(position, mazePosition)), 1);
  }

  private Set<Edge> getEdges(
      Position current, Map<Position, Node> nodes, Set<Position> seen, int length) {
    if (nodes.containsKey(current)) {
      return Set.of(new Edge(nodes.get(current), length));
    } else {
      return current.adjacent().stream()
          .filter(this::inMaze)
          .filter(
              adjacent -> {
                boolean unseen = !seen.contains(adjacent);
                seen.add(adjacent);
                return unseen;
              })
          .flatMap(adjacent -> getEdges(adjacent, nodes, seen, length + 1).stream())
          .collect(Collectors.toSet());
    }
  }

  private boolean inMaze(Position position) {
    String row = maze.get(position.y());
    return row.charAt(position.x()) == '.';
  }

  private static record NodeStart(int index, boolean startAfter, boolean inner) {

    public Optional<String> getLabel(String s) {
      char first = s.charAt(index);
      char second = s.charAt(index + 1);
      if (NON_LABEL_CHARACTERS.contains(first) || NON_LABEL_CHARACTERS.contains(second)) {
        return Optional.empty();
      } else {
        return Optional.of(String.valueOf(first) + second);
      }
    }

    public int getPositionIndex() {
      int adjustment = startAfter ? 2 : -1;
      return index + adjustment;
    }
  }
}
