package maze;

import java.util.*;

import lib.Position;

public record Path(Position key, char value, Set<Character> needed, int distance) {}
