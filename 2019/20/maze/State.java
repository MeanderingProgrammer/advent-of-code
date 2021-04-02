package maze;

import maze.path.Path;

public class State {

    private final Node node;
    private final int level;

    public State(Path path) {
        this.node = path.getLast();
        this.level = path.getLevel();
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof State) {
            State o = (State) other;
            return node.equals(o.node) && level == o.level;
        }
        return false;
    }
}
