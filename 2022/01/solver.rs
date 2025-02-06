use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let elf_items = Reader::default().groups::<String>();
    let mut elf_calories: Vec<i64> = elf_items
        .iter()
        .map(|item| item.lines().map(|s| s.parse::<i64>().unwrap()).sum())
        .collect();
    elf_calories.sort();
    elf_calories.reverse();
    answer::part1(69501, elf_calories[0]);
    answer::part2(202346, elf_calories[..3].iter().sum());
}
