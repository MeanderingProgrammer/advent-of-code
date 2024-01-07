package maze;

import java.util.*;
import lib.Position;

public record Path(Position key, char value, Set<Character> needed, int distance) {

    public boolean hasPotential(Path other) {
        // If paths are to different keys then it by definition has potential
        if (other.value != this.value) {
            return true;
        }
        boolean betterDistance = other.distance < distance;
        boolean lessKeys = !other.needed.containsAll(needed);
        return betterDistance || lessKeys;
    }
}
