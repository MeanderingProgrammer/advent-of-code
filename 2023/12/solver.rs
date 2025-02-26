use aoc::{HashMap, Reader, answer};
use std::collections::VecDeque;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum Spring {
    Operational,
    Damaged,
    Unknown,
}

impl Spring {
    fn new(ch: char) -> Self {
        match ch {
            '.' => Self::Operational,
            '#' => Self::Damaged,
            '?' => Self::Unknown,
            _ => unreachable!(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Row {
    springs: VecDeque<Spring>,
    groups: VecDeque<u8>,
}

impl FromStr for Row {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // ???.### 1,1,3
        let (springs, groups) = s.split_once(' ').unwrap();
        Ok(Self {
            springs: springs.chars().map(Spring::new).collect(),
            groups: groups.split(',').map(|ch| ch.parse().unwrap()).collect(),
        })
    }
}

impl Row {
    fn multiply(&self, n: usize) -> Self {
        let mut result = self.clone();
        for _ in 0..n - 1 {
            result.springs.push_back(Spring::Unknown);
            result.springs.append(&mut self.springs.clone());
            result.groups.append(&mut self.groups.clone());
        }
        result
    }

    fn count(self, cache: &mut HashMap<Row, usize>) -> usize {
        match cache.get(&self) {
            Some(value) => *value,
            None => {
                let value = match (self.springs.front(), self.groups.front()) {
                    (None, None) => 1,
                    (None, Some(_)) => 0,
                    (Some(_), None) => {
                        if self.springs.contains(&Spring::Damaged) {
                            0
                        } else {
                            1
                        }
                    }
                    (Some(spring), Some(group)) => match spring {
                        Spring::Operational => self.empty(cache),
                        Spring::Damaged => self.group(*group as usize, cache),
                        Spring::Unknown => self.empty(cache) + self.group(*group as usize, cache),
                    },
                };
                cache.insert(self, value);
                value
            }
        }
    }

    fn empty(&self, cache: &mut HashMap<Row, usize>) -> usize {
        let mut result = self.clone();
        result.springs.pop_front();
        result.count(cache)
    }

    fn group(&self, group: usize, cache: &mut HashMap<Row, usize>) -> usize {
        if self.any(group, Spring::Operational) || self.is(group, Spring::Damaged) {
            0
        } else {
            let mut result = self.clone();
            for _ in 0..=group {
                result.springs.pop_front();
            }
            result.groups.pop_front();
            result.count(cache)
        }
    }

    fn any(&self, n: usize, target: Spring) -> bool {
        self.springs.len() < n || self.springs.iter().take(n).any(|spring| spring == &target)
    }

    fn is(&self, n: usize, target: Spring) -> bool {
        self.springs.len() > n && self.springs[n] == target
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let rows = Reader::default().lines();
    let mut cache = HashMap::default();
    answer::part1(8075, run(&rows, &mut cache, 1));
    answer::part2(4232520187524, run(&rows, &mut cache, 5));
}

fn run(rows: &[Row], cache: &mut HashMap<Row, usize>, n: usize) -> usize {
    rows.iter().map(|row| row.multiply(n).count(cache)).sum()
}
