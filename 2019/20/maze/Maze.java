package maze;

import java.util.*;
import java.util.stream.Collectors;

public class Maze {

    private final Map<Node, Set<Edge>> graph;

    public Maze(List<String> maze) {
        graph = new MazeParser(maze).asGraph();
    }

    public int path(String start, String end, boolean recursive) {
        List<Node> startNode = getNodes(start);
        List<Node> endNode = getNodes(end);
        if (startNode.size() == 1 && endNode.size() == 1) {
            if (recursive) {
                return pathRecursive(startNode.get(0), endNode.get(0));
            } else {
                return path(startNode.get(0), endNode.get(0));
            }
        } else {
            throw new RuntimeException("Couldn't find nodes matching input");
        }
    }

    private int path(Node start, Node end) {
        PriorityQueue<Path> queue = new PriorityQueue<>();
        queue.add(new Path(start));

        Set<Node> seen = new HashSet<>();

        while (!queue.isEmpty()) {
            Path current = queue.poll();
            Node last = current.getLast();

            if (seen.contains(last)) {
                continue;
            } else {
                seen.add(last);
            }

            if (last.equals(end)) {
                return current.getLength();
            }

            for (Edge adjacent : graph.get(last)) {
                Edge opposite = getOppositeEdge(adjacent);
                if (!seen.contains(opposite.getDestination())) {
                    queue.add(current.add(opposite));
                }
            }
        }

        return -1;
    }

    private int pathRecursive(Node start, Node end) {
        // TODO: This part, probably involves making our path object store the current level
        return 0;
    }

    private Edge getOppositeEdge(Edge edge) {
        List<Node> options = getNodes(edge.getDestination().getLabel());
        if (options.size() == 1) {
            return edge;
        } else {
            Node option1 = options.get(0);
            Node option2 = options.get(1);
            Node option = option1.isInner() == edge.getDestination().isInner()
                    ? option2
                    : option1;
            return new Edge(option, edge.getLength() + 1);
        }
    }

    private List<Node> getNodes(String label) {
        return graph.keySet().stream()
                .filter(node -> node.getLabel().equals(label))
                .collect(Collectors.toList());
    }
}
