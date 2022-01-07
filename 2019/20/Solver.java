package main;

import answer.Answer;
import io.FileReader;
import maze.Maze;

public class Solver {

    private static final String FILE_NAME = "data";

    public static void main(String[] args) {
        Answer.part1(628, solve(false));
        Answer.part2(7506, solve(true));
    }

    private static int solve(boolean recursive) {
        FileReader fileReader = new FileReader(String.format("%s.txt", FILE_NAME));
        Maze maze = new Maze(fileReader.read());
        return maze.path("AA", "ZZ", recursive);
    }
}
