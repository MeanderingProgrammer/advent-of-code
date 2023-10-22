use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Backpack {
    content: String,
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
}

fn main() {
    let backpacks = reader::read(|line| Backpack {
        content: line.to_string(),
    });
    answer::part1(
        8298,
        backpacks
            .iter()
            .map(|backpack| priority(backpack.shared()))
            .sum(),
    );
    answer::part2(
        2708,
        backpacks
            .chunks(3)
            .map(|group| priority(group_overlap(group)))
            .sum(),
    );
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
        .find(|ch| group[1].content.contains(*ch) && group[2].content.contains(*ch))
        .unwrap()
}
