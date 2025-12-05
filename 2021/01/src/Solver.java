import java.util.List;

import lib.*;

public class Solver {

    public static void main(String[] args) {
        Answer.timer(() -> solution(args));
    }

    private static void solution(String[] args) {
        var values = new FileReader(args).read(Integer::parseInt);
        Answer.<Integer>part1(1292, increases(values, 1));
        Answer.<Integer>part2(1262, increases(values, 3));
    }

    private static int increases(List<Integer> values, int n) {
        var result = 0;
        for (int i = 0; i < values.size() - n; i++) {
            if (sum(values, n, i + 1) > sum(values, n, i)) {
                result++;
            }
        }
        return result;
    }

    private static int sum(List<Integer> values, int n, int start) {
        return values.subList(start, start + n).stream()
                .mapToInt(Integer::intValue)
                .sum();
    }
}
