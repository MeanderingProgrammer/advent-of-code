import lib.Answer;
import lib.FileReader;
import maze.Maze;

public class Solver {

  public static void main(String[] args) {
    var lines = new FileReader(args).read();
    Answer.part1(5402, new Maze(lines, false).complete());
    Answer.part2(2138, new Maze(lines, true).complete());
  }
}
