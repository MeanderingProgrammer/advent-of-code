package maze;

import java.util.*;
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
        grid.getKeyPositions().forEach(
                keyPosition -> expandPosition(
                        grid,
                        keyPosition,
                        grid.get(keyPosition).getValue(),
                        keyPosition,
                        new HashSet<>(),
                        0
                )
        );
    }

    private void expandPosition(
            Grid grid,
            Position keyPosition,
            Character key,
            Position position,
            Set<Character> keysNeeded,
            int distance
    ) {
        if (!grid.contains(position)) {
            return;
        }
        Node node = grid.get(position);
        if (node.isWall()) {
            return;
        }

        if (node.isDoor()) {
            keysNeeded = new HashSet<>(keysNeeded);
            keysNeeded.add(node.asKey());
        }

        Path path = new Path(keyPosition, key, keysNeeded, distance);
        if (!node.shouldGo(path)) {
            return;
        }
        node.addPath(path);

        for (Position adjacent : position.adjacent()) {
            expandPosition(grid, keyPosition, key, adjacent, keysNeeded, distance + 1);
        }
    }

    public int complete() {
        return solve(
                getStartingPositions(),
                new HashSet<>(),
                new HashMap<>()
        );
    }

    private List<Position> getStartingPositions() {
        return grids.stream()
                .map(Grid::getStartingPosition)
                .collect(Collectors.toList());
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
                if (path.canGo(keysCollected) && !keysCollected.contains(path.getKey())) {
                    List<Position> nextPositions = new ArrayList<>(positions);
                    nextPositions.set(i, path.getKeyPosition());
                    if (!cache.containsKey(nextPositions)) {
                        cache.put(nextPositions, new HashMap<>());
                    }
                    Map<Set<Character>, Integer> positionCache = cache.get(nextPositions);

                    Set<Character> nextKeys = new HashSet<>(keysCollected);
                    nextKeys.add(path.getKey());

                    int subDistance;
                    if (positionCache.containsKey(nextKeys)) {
                        subDistance = positionCache.get(nextKeys);
                    } else {
                        subDistance = solve(nextPositions, nextKeys, cache);
                        positionCache.put(nextKeys, subDistance);
                    }

                    distances.add(path.getDistance() + subDistance);
                }
            }
        }
        return Collections.min(distances);
    }

    private int totalKeys() {
        return grids.get(0).totalKeys();
    }
}
