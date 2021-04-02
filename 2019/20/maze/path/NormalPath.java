package maze.path;

import java.util.ArrayList;
import java.util.List;

import maze.Edge;
import maze.Node;

public class NormalPath implements Path, Comparable<NormalPath> {

    private final List<Edge> path;

    public NormalPath(List<Edge> path) {
        this.path = path;
    }

    public NormalPath(Node start) {
        this.path = new ArrayList<>();
        this.path.add(new Edge(start, 0));
    }

    @Override
    public NormalPath add(Edge e) {
        List<Edge> pathCopy = new ArrayList<>(path);
        pathCopy.add(e);
        return new NormalPath(pathCopy);
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
        return true;
    }

    @Override
    public int getLevel() {
        return 0;
    }

    @Override
    public int compareTo(NormalPath o) {
        return Integer.compare(getLength(), o.getLength());
    }

    @Override
    public String toString() {
        return path.toString();
    }
}
