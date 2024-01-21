use aoc_lib::answer;
use aoc_lib::reader::Reader;
use itertools::Itertools;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().read_chars();
    answer::part1(1909, first_unique_sequence(&data, 4));
    answer::part2(3380, first_unique_sequence(&data, 14));
}

fn first_unique_sequence(chars: &Vec<char>, length: usize) -> usize {
    let unique_length = |start| chars[start..start + length].iter().unique().count();
    let start_pos = (0..chars.len()).position(|i| unique_length(i) == length);
    start_pos.unwrap() + length
}
