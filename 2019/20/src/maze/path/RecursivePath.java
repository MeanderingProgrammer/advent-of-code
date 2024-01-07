package maze.path;

import java.util.*;
import maze.Edge;
import maze.Node;

/**
 * Path logic here is kind of funny, it is where we end up, not where we went through
 * This means if we see an AB inner Node to get there we went through the AB outer Node
 */
public class RecursivePath extends Path {

    public RecursivePath(Node start) {
        super(start);
    }

    private RecursivePath(List<Edge> path) {
        super(path);
    }

    @Override
    public boolean isValid() {
        if (getLevel() < 0) {
            return false;
        }
        if (isEnd(getLast()) && getLevel() != 0) {
            return false;
        }
        return true;
    }

    @Override
    protected Path newPath(List<Edge> path) {
        return new RecursivePath(path);
    }

    @Override
    protected int computeLevel() {
        List<Node> nonTerminal = path.stream()
            .map(Edge::destination)
            .filter(node -> !isEnd(node))
            .toList();
        int inner = (int) nonTerminal.stream()
            .filter(Node::inner)
            .count();
        return nonTerminal.size() - inner - inner;
    }

    private static boolean isEnd(Node node) {
        Set<String> endPoints = Set.of("AA", "ZZ");
        return endPoints.contains(node.label());
    }
}
