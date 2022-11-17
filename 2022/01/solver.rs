use aoc_lib::answer;
use aoc_lib::reader;


fn main() {
    let values = reader::read_int();
    answer::part1(window_increases(values.as_slice(), 1), 1292);
    answer::part2(window_increases(values.as_slice(), 3), 1262);
}

fn window_increases(values: &[i64], window_size: usize) -> i64 {
    let mut result = 0;
    for i in 0..values.len()-window_size {
        if window_sum(values, window_size, i + 1) > window_sum(values, window_size, i) {
            result += 1;
        }
    }
    result
}

fn window_sum(values: &[i64], window_size: usize, start_index: usize) -> i64 {
    let window = &values[start_index..start_index+window_size];
    window.iter().sum()
}
