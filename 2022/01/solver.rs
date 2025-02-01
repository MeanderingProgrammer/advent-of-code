use aoc::{answer, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let elf_items: Vec<Vec<i64>> = Reader::default().read_group_int();
    let mut elf_calories: Vec<i64> = elf_items.iter().map(|item| item.iter().sum()).collect();
    elf_calories.sort();
    elf_calories.reverse();
    answer::part1(69501, elf_calories[0]);
    answer::part2(202346, elf_calories[..3].iter().sum());
}
