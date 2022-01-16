package main;

import answer.Answer;
import io.FileReader;
import maze.Maze;

public class Solver {

    public static void main(String[] args) {
        Answer.part1(5402, solve(false));
        Answer.part2(2138, solve(true));
    }

    private static int solve(boolean splitMaze) {
        FileReader fileReader = new FileReader();
        Maze maze = new Maze(fileReader.read(), splitMaze);
        return maze.complete();
    }
}
