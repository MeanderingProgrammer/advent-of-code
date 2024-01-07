package maze;

import java.util.*;
import java.util.function.Function;
import maze.path.NormalPath;
import maze.path.Path;
import maze.path.RecursivePath;

public class Maze {

    private final Map<Node, Set<Edge>> graph;

    public Maze(List<String> maze) {
        graph = new MazeParser(maze).asGraph();
    }

    public int path(String start, String end, boolean recursive) {
        List<Node> startNode = getNodes(start);
        List<Node> endNode = getNodes(end);
        if (startNode.size() == 1 && endNode.size() == 1) {
            Function<Node, Path> pathCreator = recursive ? RecursivePath::new : NormalPath::new;
            return path(pathCreator.apply(startNode.get(0)), endNode.get(0));
        } else {
            throw new RuntimeException("Couldn't find nodes matching input");
        }
    }

    private int path(Path start, Node end) {
        PriorityQueue<Path> queue = new PriorityQueue<>();
        queue.add(start);
        Set<State> seen = new HashSet<>();
        while (!queue.isEmpty()) {
            Path current = queue.poll();
            seen.add(current.getState());
            Node last = current.getLast();
            if (last.equals(end)) {
                return current.getLength();
            }
            for (Edge adjacent : graph.get(last)) {
                Path newPath = current.add(getOppositeEdge(adjacent));
                if (!seen.contains(newPath.getState()) && newPath.isValid()) {
                    queue.add(newPath);
                }
            }
        }
        throw new RuntimeException("Couldn't find a path from start to end");
    }

    private Edge getOppositeEdge(Edge edge) {
        Node node = edge.destination();
        List<Node> options = getNodes(node.label());
        if (options.size() == 1) {
            return edge;
        } else if (options.size() == 2) {
            int index = options.get(0).equals(node) ? 1 : 0;
            return new Edge(options.get(index), edge.length() + 1);
        } else {
            throw new RuntimeException("Unexpected number of options");
        }
    }

    private List<Node> getNodes(String label) {
        return graph.keySet().stream()
            .filter(node -> node.label().equals(label))
            .toList();
    }
}
