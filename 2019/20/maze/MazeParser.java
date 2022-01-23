package maze;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

import pojo.Position;

public class MazeParser {

    private static final Set<Character> MAZE_CHARACTERS;

    static {
        MAZE_CHARACTERS = new HashSet<>();
        MAZE_CHARACTERS.add('#');
        MAZE_CHARACTERS.add('.');
        MAZE_CHARACTERS.add(' ');
    }

    private final List<String> maze;

    public MazeParser(List<String> maze) {
        this.maze = maze;
    }

    public Map<Node, Set<Edge>> asGraph() {
        Map<Node, Set<Edge>> graph = new HashMap<>();

        Set<Node> nodes = getNodes();
        for (Node node : nodes) {
            graph.put(node, getEdges(node, nodes));
        }

        return graph;
    }

    private Set<Node> getNodes() {
        Set<Node> nodes = new HashSet<>();

        for (int r = 0; r < maze.size(); r++) {
            String row = maze.get(r);
            nodes.addAll(getNodes(row, true, r));
        }

        for (int c = 0; c < maze.get(0).length(); c++) {
            String column = getColumn(c);
            nodes.addAll(getNodes(column, false, c));
        }

        return nodes;
    }

    private Set<Edge> getEdges(Node node, Set<Node> nodes) {
        Set<Edge> edges = new HashSet<>();
        for (Position next : node.getPosition().adjacent()) {
            if (inMaze(next)) {
                Set<Position> seen = new HashSet<>();
                seen.add(node.getPosition());
                edges.addAll(getEdges(next, nodes, seen, 1));
            }
        }
        return edges;
    }

    private Set<Edge> getEdges(Position current, Set<Node> nodes, Set<Position> seen, int length) {
        Set<Edge> edges = new HashSet<>();
        Optional<Node> nodeAtPosition = getNode(current, nodes);
        seen.add(current);

        if (nodeAtPosition.isPresent()) {
            edges.add(new Edge(nodeAtPosition.get(), length));
        } else {
            for (Position next : current.adjacent()) {
                if (inMaze(next) && !seen.contains(next)) {
                    edges.addAll(getEdges(next, nodes, seen, length + 1));
                }
            }
        }

        return edges;
    }

    private Optional<Node> getNode(Position position, Set<Node> nodes) {
        return nodes.stream()
                .filter(node -> node.getPosition().equals(position))
                .findFirst();
    }

    private String getColumn(int column) {
        StringBuilder result = new StringBuilder();
        for (String row : maze) {
            result.append(row.charAt(column));
        }
        return result.toString();
    }

    private Set<Node> getNodes(String rowColumn, boolean isRow, int fixedCoordinate) {
        Set<Node> nodes = new HashSet<>();
        for (NodeStart startIndex : getStartIndices(rowColumn)) {
            Optional<String> label = startIndex.getLabel(rowColumn);
            if (label.isPresent()) {
                int dynamicCoordinate = startIndex.getPositionIndex();
                Position nodePosition = isRow
                        ? new Position(dynamicCoordinate, fixedCoordinate)
                        : new Position(fixedCoordinate, dynamicCoordinate);
                nodes.add(new Node(nodePosition, label.get(), startIndex.isInner()));
            }
        }
        return nodes;
    }

    private List<NodeStart> getStartIndices(String rowColumn) {
        int totalLength = rowColumn.length();
        int mazeSize = getMazeSize();

        List<NodeStart> startIndices = new ArrayList<>();
        startIndices.add(new NodeStart(0, true, false));
        startIndices.add(new NodeStart(mazeSize + 2, false, true));
        startIndices.add(new NodeStart(totalLength - mazeSize - 4, true, true));
        startIndices.add(new NodeStart(totalLength - 2, false, false));

        return startIndices;
    }

    private int getMazeSize() {
        int middleRowIndex = maze.size() / 2;
        String middleRow = maze.get(middleRowIndex);
        return nonSpaces(middleRow) / 2;
    }

    private boolean inMaze(Position position) {
        String row = maze.get(position.getY());
        return row.charAt(position.getX()) == '.';
    }

    private static int nonSpaces(String s) {
        int nonSpaces = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch != ' ') {
                nonSpaces++;
            }
        }
        return nonSpaces;
    }

    private static class NodeStart {

        private final int index;
        private final boolean startAfter;
        private final boolean inner;

        public NodeStart(int index, boolean startAfter, boolean inner) {
            this.index = index;
            this.startAfter = startAfter;
            this.inner = inner;
        }

        public Optional<String> getLabel(String s) {
            char first = s.charAt(index);
            char second = s.charAt(index + 1);
            if (MAZE_CHARACTERS.contains(first) || MAZE_CHARACTERS.contains(second)) {
                return Optional.empty();
            } else {
                return Optional.of(
                        String.valueOf(first) + second
                );
            }
        }

        public int getPositionIndex() {
            int adjustment = startAfter ? 2 : -1;
            return index + adjustment;
        }

        public boolean isInner() {
            return inner;
        }
    }
}
