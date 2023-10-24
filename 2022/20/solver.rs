use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct SequenceEntry {
    index: usize,
    value: i64,
}

fn main() {
    answer::part1(3466, decrypt(1, 1));
    answer::part2(9995532008348, decrypt(811_589_153, 10));
}

fn decrypt(multiplier: i64, rounds: usize) -> i64 {
    let mut sequence = get_sequence(multiplier);
    let full_length = sequence.len();

    for _ in 0..rounds {
        for i in 0..sequence.len() {
            let index = sequence
                .iter()
                .position(|sequence_entry| sequence_entry.index == i)
                .unwrap();

            let entry = sequence.remove(index);
            let new_index = (index as i64 + entry.value).rem_euclid(full_length as i64 - 1);
            sequence.insert(new_index as usize, entry);
        }
    }

    let start_index = sequence
        .iter()
        .position(|sequence_entry| sequence_entry.value == 0)
        .unwrap();

    vec![1_000, 2_000, 3_000]
        .iter()
        .map(|offset| (start_index + offset) % full_length)
        .map(|index| sequence[index].value)
        .sum()
}

fn get_sequence(multiplier: i64) -> Vec<SequenceEntry> {
    reader::read_int()
        .iter()
        .enumerate()
        .map(|(index, &value)| SequenceEntry {
            index,
            value: value * multiplier,
        })
        .collect()
}
