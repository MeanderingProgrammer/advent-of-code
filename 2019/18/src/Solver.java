import lib.Answer;
import lib.FileReader;
import maze.Maze;

public class Solver {

  public static void main(String[] args) {
    Answer.part1(5402, solve(args, false));
    Answer.part2(2138, solve(args, true));
  }

  private static int solve(String[] args, boolean splitMaze) {
    FileReader fileReader = new FileReader(args);
    Maze maze = new Maze(fileReader.read(), splitMaze);
    return maze.complete();
  }
}
