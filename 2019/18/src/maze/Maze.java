package maze;

import java.util.*;

import lib.Position;

public class Maze {

    private final Grid grid;
    private final List<Position> starts;

    public Maze(List<String> maze, boolean splitMaze) {
        this.grid = new Grid(maze);

        Position start = this.grid.getStart();
        if (splitMaze) {
            this.grid.remove(start);
            start.adjacent().forEach(this.grid::remove);

            this.starts = List.of(
                    start.dx(-1).dy(-1),
                    start.dx(1).dy(-1),
                    start.dx(-1).dy(1),
                    start.dx(1).dy(1));
        } else {
            this.starts = List.of(start);
        }

        for (var key : grid.getKeys()) {
            var value = grid.get(key).getValue();
            this.expandPath(key, new Path(key, value, new HashSet<>(), 0));
        }
    }

    private void expandPath(Position position, Path path) {
        Node node = grid.get(position);
        if (node.isDoor()) {
            path = path.addKey(node.asKey());
        }
        if (!node.addPath(path)) {
            return;
        }
        for (Position adjacent : position.adjacent()) {
            if (grid.contains(adjacent)) {
                this.expandPath(adjacent, path.next());
            }
        }
    }

    public int complete() {
        var start = new State(this.starts, new HashSet<>());
        return this.solve(start, new HashMap<>());
    }

    private int solve(State state, Map<List<Position>, Map<Set<Character>, Integer>> cache) {
        if (state.values().size() == this.grid.getKeys().size()) {
            return 0;
        }
        List<Integer> distances = new ArrayList<>();
        for (Move move : this.getMoves(state)) {
            State nextState = state.move(move);
            int distance = cache
                    .computeIfAbsent(nextState.keys(), k -> new HashMap<>())
                    .computeIfAbsent(nextState.values(), k -> solve(nextState, cache));
            distances.add(move.path().distance() + distance);
        }
        return Collections.min(distances);
    }

    private List<Move> getMoves(State state) {
        List<Move> moves = new ArrayList<>();
        for (int i = 0; i < state.keys.size(); i++) {
            Node node = this.grid.get(state.keys().get(i));
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

    private static record State(List<Position> keys, Set<Character> values) {

        public State move(Move move) {
            List<Position> nextKeys = new ArrayList<>(this.keys);
            nextKeys.set(move.i(), move.path().key());
            Set<Character> nextValues = new HashSet<>(this.values);
            nextValues.add(move.path().value());
            return new State(nextKeys, nextValues);
        }
    }

    private static record Move(int i, Path path) {
    }
}
