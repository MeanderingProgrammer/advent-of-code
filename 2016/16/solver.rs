use aoc_lib::answer;
use aoc_lib::reader;

fn main() {
    answer::part1("10010101010011101", &fill_disk(272));
    answer::part2("01100111101101111", &fill_disk(35_651_584));
}

fn fill_disk(length: usize) -> String {
    let mut curve: Vec<bool> = reader::read_chars().iter().map(|&ch| ch == '1').collect();
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
