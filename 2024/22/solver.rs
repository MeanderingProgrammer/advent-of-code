use aoc_lib::answer;
use aoc_lib::collections::{HashMap, HashSet};
use aoc_lib::reader::Reader;
use rayon::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Secret {
    value: usize,
    changes: Vec<i64>,
    sequences: HashMap<[i64; 4], usize>,
}

impl FromStr for Secret {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            value: s.parse().unwrap(),
            changes: Vec::default(),
            sequences: HashMap::default(),
        })
    }
}

impl Secret {
    fn evolve(&mut self, n: usize) {
        for i in 0..n {
            let start = (self.value % 10) as i64;
            self.step();
            let finish = (self.value % 10) as i64;
            self.changes.push(finish - start);
            if i >= 3 {
                let sequence = [
                    self.changes[i - 3],
                    self.changes[i - 2],
                    self.changes[i - 1],
                    self.changes[i],
                ];
                self.sequences.entry(sequence).or_insert(finish as usize);
            }
        }
    }

    fn step(&mut self) {
        self.mix_prune(self.value * 64);
        self.mix_prune(self.value / 32);
        self.mix_prune(self.value * 2048);
    }

    fn mix_prune(&mut self, value: usize) {
        self.value ^= value;
        self.value %= 16777216;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut secrets = Reader::default().read_from_str();
    answer::part1(15608699004, part1(&mut secrets, 2000));
    answer::part2(1791, part2(&secrets));
}

fn part1(secrets: &mut [Secret], n: usize) -> usize {
    secrets
        .par_iter_mut()
        .map(|secret| {
            secret.evolve(n);
            secret.value
        })
        .sum()
}

fn part2(secrets: &[Secret]) -> usize {
    let options: HashSet<[i64; 4]> = secrets
        .iter()
        .flat_map(|secret| secret.sequences.keys())
        .cloned()
        .collect();
    options
        .par_iter()
        .map(|option| bananas(secrets, option))
        .max()
        .unwrap()
}

fn bananas(secrets: &[Secret], sequence: &[i64; 4]) -> usize {
    secrets
        .iter()
        .map(|secret| secret.sequences.get(sequence).unwrap_or(&0))
        .sum()
}
