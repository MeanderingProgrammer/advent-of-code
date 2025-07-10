use aoc::prelude::*;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values = Reader::default().lines();
    answer::part1(1292, window_increases(&values, 1));
    answer::part2(1262, window_increases(&values, 3));
}

fn window_increases(values: &[i64], window_size: usize) -> i64 {
    let mut result = 0;
    for i in 0..values.len() - window_size {
        if window_sum(values, window_size, i + 1) > window_sum(values, window_size, i) {
            result += 1;
        }
    }
    result
}

fn window_sum(values: &[i64], window_size: usize, start_index: usize) -> i64 {
    let window = &values[start_index..start_index + window_size];
    window.iter().sum()
}
