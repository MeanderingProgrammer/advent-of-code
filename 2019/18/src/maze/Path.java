package maze;

import java.util.*;
import lib.Position;

public record Path(Position keyPosition, char key, Set<Character> keysNeeded, int distance) {

  public boolean hasPotential(Path other) {
    // If paths are to different keys then it by definition has potential
    if (other.key != this.key) {
      return true;
    }
    boolean betterDistance = other.distance < distance;
    boolean lessKeys = !other.keysNeeded.containsAll(keysNeeded);
    return betterDistance || lessKeys;
  }
}
