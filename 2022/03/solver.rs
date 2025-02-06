use aoc::{answer, Reader};
use std::str::FromStr;

#[derive(Debug)]
struct Backpack {
    content: String,
}

impl FromStr for Backpack {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let content = s.to_string();
        Ok(Self { content })
    }
}

impl Backpack {
    fn compartment_1(&self) -> &str {
        &self.content[..self.content.len() / 2]
    }

    fn compartment_2(&self) -> &str {
        &self.content[self.content.len() / 2..]
    }

    fn shared(&self) -> char {
        let compartment_2 = self.compartment_2();
        self.compartment_1()
            .chars()
            .find(|ch| compartment_2.contains(*ch))
            .unwrap()
    }

    fn contains(&self, ch: &char) -> bool {
        self.content.contains(*ch)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let backpacks = Reader::default().lines::<Backpack>();

    let p1_items = backpacks.iter().map(|backpack| backpack.shared());
    answer::part1(8298, p1_items.map(priority).sum());

    let p2_items = backpacks.chunks(3).map(group_overlap);
    answer::part2(2708, p2_items.map(priority).sum());
}

fn priority(ch: char) -> u32 {
    let base = ch.to_digit(36).unwrap() - 9;
    let additional = if ch.is_uppercase() { 26 } else { 0 };
    base + additional
}

fn group_overlap(group: &[Backpack]) -> char {
    group[0]
        .content
        .chars()
        .find(|ch| group[1].contains(ch) && group[2].contains(ch))
        .unwrap()
}
