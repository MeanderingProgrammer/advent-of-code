package maze.path;

import java.util.*;

import maze.Edge;
import maze.Node;
import maze.State;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;
import lombok.experimental.PackagePrivate;

@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public abstract class Path implements Comparable<Path> {

    @PackagePrivate List<Edge> path;
    @Getter int length;
    @Getter int level;

    public Path(List<Edge> path) {
        this.path = path;
        this.length = path.stream().mapToInt(Edge::length).sum();
        this.level = computeLevel();
    }

    public Path(Node start) {
        this(List.of(new Edge(start, 0)));
    }

    public Path add(Edge e) {
        List<Edge> pathCopy = new ArrayList<>(path);
        pathCopy.add(e);
        return newPath(pathCopy);
    }

    public Node getLast() {
        return path.get(path.size() - 1).destination();
    }

    public State getState() {
        return new State(getLast(), level);
    }

    public abstract boolean isValid();

    protected abstract int computeLevel();

    protected abstract Path newPath(List<Edge> path);

    @Override
    public int compareTo(Path o) {
        return Integer.compare(getLength(), o.getLength());
    }
}
