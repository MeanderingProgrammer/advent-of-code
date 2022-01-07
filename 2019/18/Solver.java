package main;

import answer.Answer;
import io.FileReader;
import maze.Maze;

public class Solver {

    private static final String FILE_NAME = "data";

    public static void main(String[] args) {
        Answer.test();
        // Part 1: 5402
        System.out.println(String.format("Part 1: %d", solve(false)));
        // Part 2: 2138
        System.out.println(String.format("Part 2: %d", solve(true)));
    }

    private static int solve(boolean splitMaze) {
        FileReader fileReader = new FileReader(String.format("%s.txt", FILE_NAME));
        Maze maze = new Maze(fileReader.read(), splitMaze);
        return maze.complete();
    }
}
