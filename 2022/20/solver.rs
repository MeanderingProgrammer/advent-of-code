use aoc::{answer, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
struct Entry {
    index: usize,
    value: i64,
    n: usize,
}

impl Entry {
    fn new(index: usize, value: i64, length: usize) -> Self {
        Self {
            index,
            value,
            n: value.rem_euclid(length as i64 - 1) as usize,
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values = Reader::default().lines();
    answer::part1(3466, decrypt(&values, 1, 1));
    answer::part2(9995532008348, decrypt(&values, 811_589_153, 10));
}

fn decrypt(values: &[i64], key: i64, rounds: usize) -> i64 {
    let length = values.len();
    let mut sequence: VecDeque<Entry> = values
        .iter()
        .enumerate()
        .map(|(i, value)| Entry::new(i, value * key, length))
        .collect();

    for _ in 0..rounds {
        for i in 0..length {
            let index = sequence.iter().position(|entry| entry.index == i).unwrap();
            sequence.rotate_left(index);
            let entry = sequence.pop_front().unwrap();
            sequence.rotate_left(entry.n);
            sequence.push_front(entry);
        }
    }

    let start_index = sequence.iter().position(|entry| entry.value == 0).unwrap();
    [1_000, 2_000, 3_000]
        .iter()
        .map(|offset| (start_index + offset) % length)
        .map(|index| sequence[index].value)
        .sum()
}
