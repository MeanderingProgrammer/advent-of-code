package maze;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

import maze.path.NormalPath;
import maze.path.Path;
import maze.path.RecursivePath;

public class Maze {

    private final Map<Node, Set<Edge>> graph;

    public Maze(List<String> maze) {
        graph = new MazeParser(maze).asGraph();
    }

    public int path(String start, String end, boolean recursive) {
        List<Node> startNodes = getNodes(start);
        List<Node> endNodes = getNodes(end);
        if (startNodes.size() == 1 && endNodes.size() == 1) {
            Node startNode = startNodes.get(0);
            Path startPath = recursive ? new RecursivePath(startNode) : new NormalPath(startNode);
            return path(startPath, endNodes.get(0));
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
