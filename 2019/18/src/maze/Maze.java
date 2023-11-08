package maze;

import java.util.*;
import lib.Position;

public class Maze {

  private final List<Grid> grids;

  public Maze(List<String> maze, boolean splitMaze) {
    maze = new ArrayList<>(maze);
    grids = new ArrayList<>();

    Grid initialGrid = new Grid(maze);
    if (splitMaze) {
      Position startingPosition = initialGrid.getStartingPosition();
      int x = startingPosition.x();
      int y = startingPosition.y();
      MazeSplitter.split(maze, x, y);
      grids.add(new Grid(maze, new Position(x - 1, y - 1)));
      grids.add(new Grid(maze, new Position(x + 1, y - 1)));
      grids.add(new Grid(maze, new Position(x - 1, y + 1)));
      grids.add(new Grid(maze, new Position(x + 1, y + 1)));
    } else {
      grids.add(initialGrid);
    }

    grids.forEach(this::fillNodes);
  }

  private void fillNodes(Grid grid) {
    for (var keyPosition : grid.getKeyPositions()) {
      var key = grid.get(keyPosition).getValue();
      expandPosition(grid, keyPosition, key, keyPosition, new HashSet<>(), 0);
    }
  }

  private void expandPosition(
      Grid grid,
      Position keyPosition,
      char key,
      Position position,
      Set<Character> keysNeeded,
      int distance) {
    Node node = grid.get(position);

    if (node.isDoor()) {
      keysNeeded.add(node.asKey());
    }

    Path path = new Path(keyPosition, key, keysNeeded, distance);
    if (!node.shouldGo(path)) {
      return;
    }
    node.addPath(path);

    for (Position adjacent : position.adjacent()) {
      if (grid.contains(adjacent)) {
        expandPosition(grid, keyPosition, key, adjacent, new HashSet<>(keysNeeded), distance + 1);
      }
    }
  }

  public int complete() {
    List<Position> startingPositions = grids.stream().map(Grid::getStartingPosition).toList();
    return solve(new State(startingPositions, new HashSet<>()), new HashMap<>());
  }

  private int solve(State state, Map<List<Position>, Map<Set<Character>, Integer>> cache) {
    if (state.keys().size() == totalKeys()) {
      return 0;
    }

    List<Integer> distances = new ArrayList<>();
    for (Move move : getMoves(state)) {
      State nextState = state.move(move);
      int subDistance =
          cache
              .computeIfAbsent(nextState.positions(), k -> new HashMap<>())
              .computeIfAbsent(nextState.keys(), k -> solve(nextState, cache));

      distances.add(move.path().distance() + subDistance);
    }
    return Collections.min(distances);
  }

  private Set<Move> getMoves(State state) {
    Set<Move> moves = new HashSet<>();
    for (int i = 0; i < grids.size(); i++) {
      Node node = grids.get(i).get(state.positions().get(i));
      for (Path path : node.getPaths()) {
        if (state.keys().contains(path.key())) {
          continue;
        }
        if (!state.keys().containsAll(path.keysNeeded())) {
          continue;
        }
        moves.add(new Move(i, path));
      }
    }
    return moves;
  }

  private int totalKeys() {
    return grids.get(0).totalKeys();
  }

  private static record State(List<Position> positions, Set<Character> keys) {

    public State move(Move move) {
      List<Position> nextPositions = new ArrayList<>(positions);
      nextPositions.set(move.i(), move.path().keyPosition());

      Set<Character> nextKeys = new HashSet<>(keys);
      nextKeys.add(move.path().key());

      return new State(nextPositions, nextKeys);
    }
  }

  private static record Move(int i, Path path) {}
}
