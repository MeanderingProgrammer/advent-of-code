package maze;

import java.util.ArrayList;
import java.util.List;

public class Node {

    private static final Character STARTING_POINT = '@';
    private static final Character WALL = '#';

    private final Character ch;
    private final List<Path> paths;

    public Node(char ch) {
        this.ch = ch;
        this.paths = new ArrayList<>();
    }

    public Character getValue() {
        return ch;
    }

    public Character asKey() {
        if (!isDoor()) {
            throw new IllegalArgumentException("Why you asking for the key of a non-door");
        }
        return Character.toLowerCase(ch);
    }

    public boolean shouldGo(Path newPath) {
        return paths.stream()
                .allMatch(path -> path.doesPathHavePotential(newPath));
    }

    public void addPath(Path newPath) {
        paths.add(newPath);
    }

    public List<Path> getPaths() {
        return paths;
    }

    public boolean isKey() {
        return Character.isLowerCase(ch);
    }

    public boolean isDoor() {
        return Character.isUpperCase(ch);
    }

    public boolean isWall() {
        return WALL.equals(ch);
    }

    public boolean isStartingPoint() {
        return STARTING_POINT.equals(ch);
    }

    @Override
    public String toString() {
        return String.format("%s: %s", ch, paths);
    }
}
