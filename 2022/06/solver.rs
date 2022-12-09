use aoc_lib::answer;
use aoc_lib::reader;
use itertools::Itertools;

fn main() {
    let data = reader::read_chars();

    answer::part1(1909, first_unique_sequence(&data, 4));
    answer::part2(3380, first_unique_sequence(&data, 14));
}

fn first_unique_sequence(chars: &Vec<char>, length: usize) -> usize {
    (0..chars.len())
        .position(|i| &chars[i..i+length].iter().unique().count() == &length)
        .unwrap() + length
}