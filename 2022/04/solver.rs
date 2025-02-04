use aoc::{answer, Parser, Reader};
use std::str::FromStr;

#[derive(Debug)]
struct Section {
    start: i64,
    end: i64,
}

impl FromStr for Section {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let [start, end] = Parser::values(s, "-").unwrap();
        Ok(Self { start, end })
    }
}

impl Section {
    fn contains_all(&self, other: &Section) -> bool {
        self.start <= other.start && self.end >= other.end
    }

    fn contains_any(&self, other: &Section) -> bool {
        let max_start = self.start.max(other.start);
        let min_end = self.end.min(other.end);
        max_start <= min_end
    }
}

#[derive(Debug)]
struct Assignment {
    first: Section,
    second: Section,
}

impl FromStr for Assignment {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let [first, second] = Parser::values(s, ",").unwrap();
        Ok(Self { first, second })
    }
}

impl Assignment {
    fn full_overlap(&self) -> bool {
        self.first.contains_all(&self.second) || self.second.contains_all(&self.first)
    }

    fn any_overlap(&self) -> bool {
        self.first.contains_any(&self.second)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let assignments = Reader::default().read_from_str();
    answer::part1(532, get_count(&assignments, Assignment::full_overlap));
    answer::part2(854, get_count(&assignments, Assignment::any_overlap));
}

fn get_count(assignments: &[Assignment], f: fn(&Assignment) -> bool) -> usize {
    assignments
        .iter()
        .filter(|assignment| f(assignment))
        .count()
}
