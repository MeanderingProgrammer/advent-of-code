package maze;

import java.util.Set;

import pojo.Position;

public class Path {

    private final Position keyPosition;
    private final Character key;
    private final Set<Character> keysNeeded;
    private final int distance;

    public Path(Position keyPosition, Character key, Set<Character> keysNeeded, int distance) {
        this.keyPosition = keyPosition;
        this.key = key;
        this.keysNeeded = keysNeeded;
        this.distance = distance;
    }

    public boolean doesPathHavePotential(Path other) {
        // If paths are to different keys then it by definition has potential
        if (!other.key.equals(key)) {
            return true;
        }
        boolean betterDistance = other.distance < distance;
        boolean lessKeys = !other.keysNeeded.containsAll(keysNeeded);
        return betterDistance || lessKeys;
    }

    public boolean canGo(Set<Character> keysCollected) {
        return keysCollected.containsAll(keysNeeded);
    }

    public Position getKeyPosition() {
        return keyPosition;
    }

    public Character getKey() {
        return key;
    }

    public Set<Character> getKeysNeeded() {
        return keysNeeded;
    }

    public int getDistance() {
        return distance;
    }

    @Override
    public String toString() {
        return String.format("To %s at %s In %s if %s are present", key, keyPosition, distance, keysNeeded);
    }
}
