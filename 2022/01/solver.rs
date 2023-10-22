use aoc_lib::answer;
use aoc_lib::reader;

fn main() {
    let elf_items: Vec<Vec<i64>> = reader::read_group_int();
    let mut elf_calories: Vec<i64> = elf_items.iter().map(|item| item.iter().sum()).collect();
    elf_calories.sort();
    elf_calories.reverse();
    answer::part1(69501, elf_calories[0]);
    answer::part2(202346, elf_calories[..3].iter().sum());
}
