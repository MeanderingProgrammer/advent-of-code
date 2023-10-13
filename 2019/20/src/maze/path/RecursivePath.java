package maze.path;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import com.google.common.collect.Sets;

import maze.Edge;
import maze.Node;

/**
 * Path logic here is kind of funny, it is where we end up, not where we went through.
 * This means if we see an AB inner Node to get there we went through the AB outer Node.
 */
public class RecursivePath extends Path {

    private static final Set<String> END_POINTS = Sets.newHashSet("AA", "ZZ");

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
            .map(Edge::getDestination)
            .filter(node -> !isEnd(node))
            .collect(Collectors.toList());
        
        int inner = (int) nonTerminal.stream()
            .filter(Node::isInner)
            .count();
        
        return nonTerminal.size() - inner - inner;
    }

    private static boolean isEnd(Node node) {
        return END_POINTS.contains(node.getLabel());
    }
}
