use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug)]
struct Stats {
    latest: i64,
    previous: Option<i64>,
}

impl Stats {
    fn new(turn: usize) -> Self {
        Self {
            latest: turn.try_into().unwrap(),
            previous: None,
        }
    }

    fn next(&self) -> i64 {
        match self.previous {
            Some(value) => self.latest - value,
            None => 0,
        }
    }

    fn said(&mut self, turn: usize) {
        self.previous = Some(self.latest);
        self.latest = turn.try_into().unwrap();
    }
}

fn main() {
    let starting_numbers = reader::read_csv();
    answer::part1(240, run(&starting_numbers, 2_020));
    answer::part2(505, run(&starting_numbers, 30_000_000));
}

fn run(starting_numbers: &Vec<i64>, n: usize) -> u32 {
    let mut number_stats: HashMap<i64, Stats> = HashMap::new();
    starting_numbers.iter().enumerate().for_each(|(i, value)| {
        number_stats.insert(value.clone(), Stats::new(i));
    });

    let mut number: i64 = *starting_numbers.last().unwrap();
    for i in starting_numbers.len()..n {
        number = number_stats.get(&number).unwrap().next();
        match number_stats.get_mut(&number) {
            Some(stats) => stats.said(i),
            None => {
                number_stats.insert(number, Stats::new(i));
            }
        };
    }
    number.try_into().unwrap()
}
