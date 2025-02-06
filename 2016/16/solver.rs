use aoc::{answer, Iter, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let curve = Reader::default()
        .chars::<char>()
        .into_iter()
        .map(|ch| ch == '1')
        .vec();
    answer::part1("10010101010011101", &fill_disk(curve.clone(), 272));
    answer::part2("01100111101101111", &fill_disk(curve.clone(), 35_651_584));
}

fn fill_disk(mut curve: Vec<bool>, length: usize) -> String {
    while curve.len() < length {
        let mut flipped: Vec<bool> = curve.iter().rev().map(|value| !value).collect();
        curve.push(false);
        curve.append(&mut flipped);
    }
    get_checksum(&curve[..length])
        .into_iter()
        .map(|value| if value { '1' } else { '0' })
        .collect()
}

fn get_checksum(value: &[bool]) -> Vec<bool> {
    let checksum: Vec<bool> = (0..value.len())
        .step_by(2)
        .map(|i| value[i] == value[i + 1])
        .collect();
    if checksum.len() % 2 == 1 {
        checksum
    } else {
        get_checksum(&checksum)
    }
}
