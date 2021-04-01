package maze;

public class Edge {

    private final Node destination;
    private final int length;

    public Edge(Node destination, int length) {
        this.destination = destination;
        this.length = length;
    }

    public Node getDestination() {
        return destination;
    }

    public int getLength() {
        return length;
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof Edge) {
            Edge o = (Edge) other;
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
        return String.format("To %s in %d", destination.toString(), length);
    }
}
