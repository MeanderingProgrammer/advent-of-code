package maze;

import pojo.Position;

public class Node {

    private final Position position;
    private final String label;
    private final boolean inner;

    public Node(Position position, String label, boolean inner) {
        this.position = position;
        this.label = label;
        this.inner = inner;
    }

    public Position getPosition() {
        return position;
    }

    public String getLabel() {
        return label;
    }

    public boolean isInner() {
        return inner;
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof Node) {
            Node o = (Node) other;
            return toString().equals(o.toString());
        }
        return false;
    }

    @Override
    public int hashCode() {
        return toString().hashCode();
    }

    @Override
    public String toString() {
        String side = inner ? "inside" : "outside";
        return String.format("%s %s @ %s", label, side, position.toString());
    }
}
