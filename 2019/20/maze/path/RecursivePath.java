package maze.path;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import maze.Edge;
import maze.Node;

/**
 * Path logic here is kind of funny, it is where we end up, not where we went through.
 * This means if we see an AB inner Node to get there we went through the AB outer Node.
 */
public class RecursivePath implements Path, Comparable<RecursivePath> {

    private static final Set<String> END_POINTS;

    static {
        END_POINTS = new HashSet<>();
        END_POINTS.add("AA");
        END_POINTS.add("ZZ");
    }

    private final List<Edge> path;

    public RecursivePath(List<Edge> path) {
        this.path = path;
    }

    public RecursivePath(Node start) {
        this.path = new ArrayList<>();
        this.path.add(new Edge(start, 0));
    }

    @Override
    public RecursivePath add(Edge e) {
        List<Edge> pathCopy = new ArrayList<>(path);
        pathCopy.add(e);
        return new RecursivePath(pathCopy);
    }

    @Override
    public Node getLast() {
        return path.get(path.size() - 1).getDestination();
    }

    @Override
    public int getLength() {
        return path.stream()
                .mapToInt(Edge::getLength)
                .sum();
    }

    @Override
    public boolean isValid() {
        int level = getLevel();
        if (level < 0) {
            return false;
        }
        if (isEnd() && level != 0) {
            return false;
        }
        return true;
    }

    @Override
    public int getLevel() {
        int level = 0;
        for (Edge edge : path) {
            if (!isEnd(edge.getDestination().getLabel())) {
                if (edge.getDestination().isInner()) {
                    // If we are at an inner node that means we went through an outer node
                    level--;
                } else {
                    level++;
                }
            }
        }
        return level;
    }

    @Override
    public int compareTo(RecursivePath o) {
        return Integer.compare(getLength(), o.getLength());
    }

    @Override
    public String toString() {
        return path.toString();
    }

    private boolean isEnd() {
        return isEnd(getLast().getLabel());
    }

    private static boolean isEnd(String label) {
        return END_POINTS.contains(label);
    }
}
