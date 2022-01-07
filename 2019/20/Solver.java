package main;

import io.FileReader;
import maze.Maze;

public class Solver {

    private static final String FILE_NAME = "data";

    public static void main(String[] args) {
        // Part 1: 628
        System.out.println(String.format("Part 1: %d", solve(false)));
        // Part 2: 7506
        System.out.println(String.format("Part 2: %d", solve(true)));
    }

    private static int solve(boolean recursive) {
        FileReader fileReader = new FileReader(String.format("%s.txt", FILE_NAME));
        Maze maze = new Maze(fileReader.read());
        return maze.path("AA", "ZZ", recursive);
    }
}
