package maze;

import java.util.Set;

import pojo.Position;


import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.experimental.FieldDefaults;

@Getter
@AllArgsConstructor
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Path {

    Position keyPosition;
    char key;
    Set<Character> keysNeeded;
    int distance;

    public boolean hasPotential(Path other) {
        // If paths are to different keys then it by definition has potential
        if (other.key != this.key) {
            return true;
        }
        boolean betterDistance = other.distance < distance;
        boolean lessKeys = !other.keysNeeded.containsAll(keysNeeded);
        return betterDistance || lessKeys;
    }

    public boolean canGo(Set<Character> keysCollected) {
        return keysCollected.containsAll(keysNeeded);
    }
}
