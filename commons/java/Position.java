package pojo;

import java.util.HashSet;
import java.util.Set;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.ToString;
import lombok.experimental.FieldDefaults;

@Getter
@ToString
@EqualsAndHashCode
@AllArgsConstructor
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
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
