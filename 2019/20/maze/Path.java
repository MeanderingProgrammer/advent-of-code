package maze;

import java.util.ArrayList;
import java.util.List;

public class Path implements Comparable<Path> {

    private final List<Edge> path;

    public Path(List<Edge> path) {
        this.path = path;
    }

    public Path(Node start) {
        this.path = new ArrayList<>();
        this.path.add(new Edge(start, 0));
    }

    public Path add(Edge e) {
        List<Edge> pathCopy = new ArrayList<>(path);
        pathCopy.add(e);
        return new Path(pathCopy);
    }

    public Node getLast() {
        return path.get(path.size() - 1).getDestination();
    }

    public int getLength() {
        return path.stream()
                .mapToInt(Edge::getLength)
                .sum();
    }

    @Override
    public int compareTo(Path o) {
        return Integer.compare(getLength(), o.getLength());
    }

    @Override
    public String toString() {
        return path.toString();
    }
}
