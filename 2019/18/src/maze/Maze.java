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
            Position startingPosition = initialGrid.getStart();
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
        for (var key : grid.getKeys()) {
            var value = grid.get(key).getValue();
            expandPosition(grid, key, value, key, new HashSet<>(), 0);
        }
    }

    private void expandPosition(
        Grid grid, 
        Position key, 
        char value, 
        Position position, 
        Set<Character> needed, 
        int distance
    ) {
        Node node = grid.get(position);
        if (node.isDoor()) {
            needed.add(node.asKey());
        }
        Path path = new Path(key, value, needed, distance);
        if (!node.addPath(path)) {
            return;
        }
        for (Position adjacent : position.adjacent()) {
            if (grid.contains(adjacent)) {
                expandPosition(grid, key, value, adjacent, new HashSet<>(needed), distance + 1);
            }
        }
    }

    public int complete() {
        var keys = grids.stream().map(Grid::getStart).toList();
        var state = new State(keys, new HashSet<>());
        return solve(state, new HashMap<>());
    }

    private int solve(State state, Map<List<Position>, Map<Set<Character>, Integer>> cache) {
        if (state.values().size() == totalKeys()) {
            return 0;
        }
        List<Integer> distances = new ArrayList<>();
        for (Move move : getMoves(state)) {
            State nextState = state.move(move);
            int distance = cache
                .computeIfAbsent(nextState.keys(), k -> new HashMap<>())
                .computeIfAbsent(nextState.values(), k -> solve(nextState, cache));
            distances.add(move.path().distance() + distance);
        }
        return Collections.min(distances);
    }

    private Set<Move> getMoves(State state) {
        Set<Move> moves = new HashSet<>();
        for (int i = 0; i < grids.size(); i++) {
            Node node = grids.get(i).get(state.keys().get(i));
            for (Path path : node.getPaths()) {
                if (state.values().contains(path.value())) {
                    continue;
                }
                if (!state.values().containsAll(path.needed())) {
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

    private static record State(List<Position> keys, Set<Character> values) {

        public State move(Move move) {
            List<Position> nextKeys = new ArrayList<>(keys);
            nextKeys.set(move.i(), move.path().key());
            Set<Character> nextValues = new HashSet<>(values);
            nextValues.add(move.path().value());
            return new State(nextKeys, nextValues);
        }
    }

    private static record Move(int i, Path path) {}
}
