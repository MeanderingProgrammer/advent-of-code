package lib;

import java.util.Set;

import com.google.common.collect.Sets;

import lombok.Value;

@Value
public class Position {

    int x;
    int y;

    public Set<Position> adjacent() {
        return Sets.newHashSet(
            new Position(x+1, y),
            new Position(x-1, y),
            new Position(x, y+1),
            new Position(x, y-1)
        );
    }
}
