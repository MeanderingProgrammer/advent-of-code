use aoc::{Iter, Reader, Str, answer};
use std::collections::VecDeque;
use std::fmt;
use std::str::FromStr;

#[derive(Debug)]
enum Instruction {
    Spin(usize),
    Exchange(usize, usize),
    Partner(char, char),
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // s11 | x10/2 | pa/i
        let (op, s) = (&s[..1], &s[1..]);
        match op {
            "s" => Ok(Self::Spin(s.parse().unwrap())),
            "x" => {
                let (l, r) = s.split_once('/').unwrap();
                Ok(Self::Exchange(l.parse().unwrap(), r.parse().unwrap()))
            }
            "p" => {
                let (l, r) = s.split_once('/').unwrap();
                Ok(Self::Partner(Str::first(l), Str::first(r)))
            }
            _ => Err(format!("Uknown op: {op}")),
        }
    }
}

#[derive(Debug)]
struct Dance {
    dancers: VecDeque<char>,
}

impl Default for Dance {
    fn default() -> Self {
        Self {
            dancers: ('a'..='z').take(16).collect(),
        }
    }
}

impl fmt::Display for Dance {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.dancers.iter().join(""))
    }
}

impl Dance {
    fn perform(&mut self, instructions: &[Instruction]) {
        instructions
            .iter()
            .for_each(|instruction| self.step(instruction));
    }

    fn step(&mut self, instruction: &Instruction) {
        match instruction {
            Instruction::Spin(n) => self.dancers.rotate_right(*n),
            Instruction::Exchange(i1, i2) => self.dancers.swap(*i1, *i2),
            Instruction::Partner(d1, d2) => self.dancers.swap(self.find(d1), self.find(d2)),
        }
    }

    fn find(&self, target: &char) -> usize {
        self.dancers.iter().position(|d| d == target).unwrap()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions = Reader::default().csv();
    let pattern = get_pattern(&instructions);
    answer::part1("eojfmbpkldghncia", &pattern[1]);
    answer::part2("iecopnahgdflmkjb", &pattern[1_000_000_000 % pattern.len()]);
}

fn get_pattern(instructions: &[Instruction]) -> Vec<String> {
    let mut dance = Dance::default();
    let mut pattern = Vec::default();
    while !pattern.contains(&dance.to_string()) {
        pattern.push(dance.to_string());
        dance.perform(instructions);
    }
    pattern
}
