package maze;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;

@Getter
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Node {

    char value;
    Set<Path> paths;

    public Node(char value) {
        this.value = value;
        this.paths = new HashSet<>();
    }

    public char asKey() {
        if (!isDoor()) {
            throw new IllegalArgumentException("Why you asking for the key of a non-door");
        }
        return Character.toLowerCase(value);
    }

    public boolean addPath(Path newPath) {
        if (shouldGo(newPath)) {
            paths.add(newPath);
            return true;
        } else {
            return false;
        }
    }

    private boolean shouldGo(Path newPath) {
        var remove = new ArrayList<>();
        var result = paths.stream()
                // Get all existing paths we have to the same key
                .filter(path -> path.value() == newPath.value())
                .allMatch(path -> {
                    if (newPath.distance() < path.distance()) {
                        // New path does not require any more keys than the existing path
                        if (path.needed().containsAll(newPath.needed())) {
                            remove.add(path);
                        }
                        return true;
                    } else {
                        // New path does not require every key required by the existing path
                        return !newPath.needed().containsAll(path.needed());
                    }
                });
        remove.forEach(this.paths::remove);
        return result;
    }

    public boolean isKey() {
        return Character.isLowerCase(value);
    }

    public boolean isDoor() {
        return Character.isUpperCase(value);
    }

    public boolean isStart() {
        return '@' == value;
    }
}
