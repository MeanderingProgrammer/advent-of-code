use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Elf {
    items: Vec<i64>,
}

impl FromStr for Elf {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let items = s.lines().map(|item| item.parse().unwrap()).collect();
        Ok(Self { items })
    }
}

impl Elf {
    fn calories(&self) -> i64 {
        self.items.iter().sum()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let elfs = Reader::default().groups::<Elf>();
    let calories = elfs
        .iter()
        .map(|elf| elf.calories())
        .sorted()
        .rev()
        .collect::<Vec<_>>();
    answer::part1(69501, calories[0]);
    answer::part2(202346, calories[..3].iter().sum());
}
