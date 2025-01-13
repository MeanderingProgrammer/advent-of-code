import lib.*;

public class Solver {

    public static void main(String[] args) {
        Answer.timer(() -> solution(args));
    }

    private static void solution(String[] args) {
        FileReader fileReader = new FileReader(args);
        System.out.println(fileReader.read());
        Answer.<Integer>part1(1, 1);
        Answer.<Integer>part2(1, 1);
    }
}
