use aoc::prelude::*;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values = Reader::default().lines();
    answer::part1(1292, increases(&values, 1));
    answer::part2(1262, increases(&values, 3));
}

fn increases(values: &[i64], n: usize) -> i64 {
    let mut result = 0;
    for i in 0..values.len() - n {
        if sum(values, n, i + 1) > sum(values, n, i) {
            result += 1;
        }
    }
    result
}

fn sum(values: &[i64], n: usize, start: usize) -> i64 {
    values[start..start + n].iter().sum()
}
