import lib.Answer;
import lib.FileReader;
import maze.Maze;

public class Solver {

    public static void main(String[] args) {
        Answer.timer(() -> solution(args));
    }

    private static void solution(String[] args) {
        var lines = new FileReader(args).read();
        Answer.<Integer>part1(5402, new Maze(lines, false).complete());
        Answer.<Integer>part2(2138, new Maze(lines, true).complete());
    }
}
