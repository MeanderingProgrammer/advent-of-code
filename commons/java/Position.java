package pojo;

import java.util.HashSet;
import java.util.Set;

import lombok.Value;

@Value
public class Position {

    int x;
    int y;

    public Set<Position> adjacent() {
        Set<Position> result = new HashSet<>();
        result.add(new Position(x+1, y));
        result.add(new Position(x-1, y));
        result.add(new Position(x, y+1));
        result.add(new Position(x, y-1));
        return result;
    }
}
