package maze.path;

import maze.Edge;
import maze.Node;

public interface Path {

    Path add(Edge e);
    Node getLast();
    int getLength();
    boolean isValid();
    int getLevel();
}
