use aoc::{Reader, answer};
use std::str::FromStr;

#[derive(Debug)]
struct Section {
    start: i64,
    end: i64,
}

impl FromStr for Section {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (start, end) = s.split_once('-').unwrap();
        Ok(Self {
            start: start.parse().unwrap(),
            end: end.parse().unwrap(),
        })
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
        let (first, second) = s.split_once(',').unwrap();
        Ok(Self {
            first: first.parse().unwrap(),
            second: second.parse().unwrap(),
        })
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
    let assignments = Reader::default().lines();
    answer::part1(532, get_count(&assignments, Assignment::full_overlap));
    answer::part2(854, get_count(&assignments, Assignment::any_overlap));
}

fn get_count(assignments: &[Assignment], f: fn(&Assignment) -> bool) -> usize {
    assignments
        .iter()
        .filter(|assignment| f(assignment))
        .count()
}
