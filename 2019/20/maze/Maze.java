package maze;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

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
            Function<Node, Path> pathCreator = recursive
                    ? RecursivePath::new
                    : NormalPath::new;

            return path(startNode.get(0), endNode.get(0), pathCreator);
        } else {
            throw new RuntimeException("Couldn't find nodes matching input");
        }
    }

    private int path(Node start, Node end, Function<Node, Path> pathCreator) {
        PriorityQueue<Path> queue = new PriorityQueue<>();
        queue.add(pathCreator.apply(start));

        Set<State> seen = new HashSet<>();

        while (!queue.isEmpty()) {
            Path current = queue.poll();
            State currentState = new State(current);

            if (seen.contains(currentState)) {
                continue;
            } else {
                seen.add(currentState);
            }

            Node last = current.getLast();
            if (last.equals(end)) {
                return current.getLength();
            }

            for (Edge adjacent : graph.get(last)) {
                Path newPath = current.add(getOppositeEdge(adjacent));
                State newState = new State(newPath);

                if (!seen.contains(newState) && newPath.isValid()) {
                    queue.add(newPath);
                }
            }
        }

        return -1;
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
