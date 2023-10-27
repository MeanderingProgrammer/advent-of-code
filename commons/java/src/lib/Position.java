package lib;

import java.util.*;

public record Position(int x, int y) {

  public Set<Position> adjacent() {
    return Set.of(
        new Position(x + 1, y),
        new Position(x - 1, y),
        new Position(x, y + 1),
        new Position(x, y - 1));
  }
}
