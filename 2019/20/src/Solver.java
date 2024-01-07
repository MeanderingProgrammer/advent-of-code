import lib.Answer;
import lib.FileReader;
import maze.Maze;

public class Solver {

    public static void main(String[] args) {
        Answer.timer(() -> solution(args));
    }

    private static void solution(String[] args) {
        Maze maze = new Maze(new FileReader(args).read());
        Answer.part1(628, solve(maze, false));
        Answer.part2(7506, solve(maze, true));
    }

    private static int solve(Maze maze, boolean recursive) {
        return maze.path("AA", "ZZ", recursive);
    }
}
