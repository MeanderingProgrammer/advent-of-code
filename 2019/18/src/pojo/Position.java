package pojo;

import java.util.ArrayList;
import java.util.List;

public class Position {

    private final int x;
    private final int y;

    public Position(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public List<Position> adjacent() {
        List<Position> result = new ArrayList<>();
        result.add(new Position(x+1, y));
        result.add(new Position(x-1, y));
        result.add(new Position(x, y+1));
        result.add(new Position(x, y-1));
        return result;
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof Position) {
            Position o = (Position) other;
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
        return String.format("(%d, %d)", this.x, this.y);
    }
}
