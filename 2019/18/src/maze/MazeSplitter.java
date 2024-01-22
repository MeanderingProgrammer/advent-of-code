package maze;

import java.util.List;

public class MazeSplitter {

    public static void split(List<String> maze, int x, int y) {
        update(maze, x, y - 1, '#');
        update(maze, x - 1, y, '#');
        update(maze, x, y, '#');
        update(maze, x + 1, y, '#');
        update(maze, x, y + 1, '#');

        update(maze, x - 1, y - 1, '@');
        update(maze, x - 1, y + 1, '@');
        update(maze, x + 1, y - 1, '@');
        update(maze, x + 1, y + 1, '@');
    }

    private static void update(List<String> maze, int x, int y, char ch) {
        String row = maze.get(y);
        char[] rowCharacters = row.toCharArray();
        rowCharacters[x] = ch;
        maze.set(y, String.valueOf(rowCharacters));
    }
}
