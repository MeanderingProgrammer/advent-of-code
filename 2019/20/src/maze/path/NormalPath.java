package maze.path;

import java.util.*;
import maze.Edge;
import maze.Node;

public class NormalPath extends Path {

    public NormalPath(Node start) {
        super(start);
    }

    private NormalPath(List<Edge> path) {
        super(path);
    }

    @Override
    public boolean isValid() {
        return true;
    }

    @Override
    protected Path newPath(List<Edge> path) {
        return new NormalPath(path);
    }

    @Override
    protected int computeLevel() {
        return 0;
    }
}
