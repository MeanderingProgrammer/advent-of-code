package maze;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import pojo.Position;

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
        return solve(startingPositions, new HashSet<>(), new HashMap<>());
    }

    private int solve(
            List<Position> positions,
            Set<Character> keysCollected,
            Map<List<Position>, Map<Set<Character>, Integer>> cache
    ) {
        if (totalKeys() == keysCollected.size()) {
            return 0;
        }

        List<Integer> distances = new ArrayList<>();
        for (int i = 0; i < grids.size(); i++) {
            for (Path path : grids.get(i).get(positions.get(i)).getPaths()) {
                if (!path.canGo(keysCollected) || keysCollected.contains(path.getKey())) {
                    continue;
                }

                List<Position> nextPositions = new ArrayList<>(positions);
                nextPositions.set(i, path.getKeyPosition());

                Set<Character> nextKeys = new HashSet<>(keysCollected);
                nextKeys.add(path.getKey());

                int subDistance = cache
                    .computeIfAbsent(nextPositions, k -> new HashMap<>())
                    .computeIfAbsent(nextKeys, k -> solve(nextPositions, k, cache));

                distances.add(path.getDistance() + subDistance);
            }
        }
        return Collections.min(distances);
    }

    private int totalKeys() {
        return grids.get(0).totalKeys();
    }
}
