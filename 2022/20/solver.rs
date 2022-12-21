use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct SequenceEntry {
    index: i64,
    value: i64,
}

fn main() {
    answer::part1(3466, decrypt(1, 1));
    answer::part2(9995532008348, decrypt(811_589_153, 10));
}

fn decrypt(multiplier: i64, rounds: usize) -> i64 {
    let mut sequence = get_sequence(multiplier);
    let full_length = i64::try_from(sequence.len()).unwrap();

    for _ in 0..rounds {
        for i in 0..sequence.len() {
            let index = sequence.iter()
                .position(|sequence_entry| sequence_entry.index == to_int(i))
                .unwrap();
            
            let entry = sequence.remove(index);
            let new_index = (to_int(index) + entry.value).rem_euclid(full_length - 1);
            sequence.insert(to_index(new_index), entry);
        }
    }

    let start_index = sequence.iter()
        .position(|sequence_entry| sequence_entry.value == 0)
        .unwrap();
    
    vec![1_000, 2_000, 3_000].iter()
        .map(|offset| (to_int(start_index) + offset) % full_length)
        .map(|index| sequence[to_index(index)].value)
        .sum()
}

fn get_sequence(multiplier: i64) -> Vec<SequenceEntry> {
    reader::read_int().iter().enumerate()
        .map(|(index, &value)| SequenceEntry { 
            index: to_int(index), 
            value: value * multiplier,
        })
        .collect()
}

fn to_int(value: usize) -> i64 {
    i64::try_from(value).unwrap()
}

fn to_index(value: i64) -> usize {
    usize::try_from(value).unwrap()
}
