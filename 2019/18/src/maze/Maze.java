package maze;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import lib.Position;

import lombok.Value;

public class Maze {

    private final List<Grid> grids;

    public Maze(List<String> maze, boolean splitMaze) {
        grids = new ArrayList<>();

        Grid initialGrid = new Grid(maze);
        if (splitMaze) {
            Position startingPosition = initialGrid.getStartingPosition();
            int x = startingPosition.getX();
            int y = startingPosition.getY();
            MazeSplitter.split(maze, x, y);
            grids.add(new Grid(maze, new Position(x-1, y-1)));
            grids.add(new Grid(maze, new Position(x+1, y-1)));
            grids.add(new Grid(maze, new Position(x-1, y+1)));
            grids.add(new Grid(maze, new Position(x+1, y+1)));
        } else {
            grids.add(initialGrid);
        }

        grids.forEach(this::fillNodes);
    }

    private void fillNodes(Grid grid) {
        grid.getKeyPositions()
            .forEach(keyPosition -> expandPosition(
                grid,
                keyPosition,
                grid.get(keyPosition).getValue(),
                keyPosition,
                new HashSet<>(),
                0
            ));
    }

    private void expandPosition(
            Grid grid,
            Position keyPosition,
            char key,
            Position position,
            Set<Character> keysNeeded,
            int distance
    ) {
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
        List<Position> startingPositions = grids.stream()
            .map(Grid::getStartingPosition)
            .collect(Collectors.toList());
        return solve(new State(startingPositions, new HashSet<>()), new HashMap<>());
    }

    private int solve(State state, Map<List<Position>, Map<Set<Character>, Integer>> cache) {
        if (state.getKeys().size() == totalKeys()) {
            return 0;
        }

        List<Integer> distances = new ArrayList<>();
        for (Move move : getMoves(state)) {
            State nextState = state.move(move);
            int subDistance = cache
                .computeIfAbsent(nextState.getPositions(), k -> new HashMap<>())
                .computeIfAbsent(nextState.getKeys(), k -> solve(nextState, cache));

            distances.add(move.getPath().getDistance() + subDistance);
        }
        return Collections.min(distances);
    }

    private Set<Move> getMoves(State state) {
        Set<Move> moves = new HashSet<>();
        for (int i = 0; i < grids.size(); i++) {
            Node node = grids.get(i).get(state.getPositions().get(i));
            for (Path path : node.getPaths()) {
                if (state.getKeys().contains(path.getKey())) {
                    continue;
                }
                if (!state.getKeys().containsAll(path.getKeysNeeded())) {
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

    @Value
    private static class State {

        List<Position> positions;
        Set<Character> keys;

        public State move(Move move) {
            List<Position> nextPositions = new ArrayList<>(positions);
            nextPositions.set(move.getI(), move.getPath().getKeyPosition());

            Set<Character> nextKeys = new HashSet<>(keys);
            nextKeys.add(move.getPath().getKey());

            return new State(nextPositions, nextKeys);
        }
    }

    @Value
    private static class Move {
        int i;
        Path path;
    }
}
