package maze;

import java.util.HashSet;
import java.util.Set;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.experimental.FieldDefaults;

@Getter
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
public class Node {

  private static final Character STARTING_POINT = '@';

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

  public boolean shouldGo(Path newPath) {
    return paths.stream().allMatch(path -> path.hasPotential(newPath));
  }

  public void addPath(Path newPath) {
    paths.add(newPath);
  }

  public boolean isKey() {
    return Character.isLowerCase(value);
  }

  public boolean isDoor() {
    return Character.isUpperCase(value);
  }

  public boolean isStartingPoint() {
    return STARTING_POINT == value;
  }
}
