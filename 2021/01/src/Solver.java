import java.util.List;

import lib.*;

public class Solver {

    public static void main(String[] args) {
        Answer.timer(() -> solution(args));
    }

    private static void solution(String[] args) {
        var values = new FileReader(args).read(Integer::parseInt);
        Answer.<Integer>part1(1292, windowIncreases(values, 1));
        Answer.<Integer>part2(1262, windowIncreases(values, 3));
    }

    private static int windowIncreases(List<Integer> values, int windowSize) {
        var increases = 0;
        for (int i = 0; i < values.size() - windowSize; i++) {
            if (sum(values, windowSize, i + 1) > sum(values, windowSize, i)) {
                increases++;
            }
        }
        return increases;
    }

    private static int sum(List<Integer> values, int windowSize, int start) {
        return values.subList(start, start + windowSize).stream()
                .mapToInt(Integer::intValue)
                .sum();
    }
}
