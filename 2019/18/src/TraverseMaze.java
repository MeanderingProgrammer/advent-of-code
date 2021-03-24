import io.FileReader;
import maze.Maze;

public class TraverseMaze {

    public static void main(String[] args) {
        String fileName = "data";
        // Part 1 = 5402
        solve(fileName, false);
        // Part 2 = 2138
        solve(fileName, true);
    }

    private static void solve(String fileName, boolean splitMaze) {
        FileReader fileReader = new FileReader(String.format("%s.txt", fileName));
        Maze maze = new Maze(fileReader.read(), splitMaze);
        int totalDistance = maze.complete();
        System.out.println(String.format("Total distance travelled = %d", totalDistance));
    }
}
