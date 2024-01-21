use aoc_lib::answer;
use aoc_lib::reader::Reader;

#[derive(Debug, Clone)]
struct Stats {
    latest: usize,
    previous: Option<usize>,
}

impl Stats {
    fn new(turn: usize) -> Self {
        Self {
            latest: turn,
            previous: None,
        }
    }

    fn next(&self) -> usize {
        match self.previous {
            Some(value) => self.latest - value,
            None => 0,
        }
    }

    fn said(&mut self, turn: usize) {
        self.previous = Some(self.latest);
        self.latest = turn;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values = Reader::default()
        .read_csv()
        .into_iter()
        .map(|value| value as usize)
        .collect();
    answer::part1(240, run(&values, 2_020));
    answer::part2(505, run(&values, 30_000_000));
}

fn run(values: &Vec<usize>, n: usize) -> usize {
    let mut number_stats: Vec<Option<Stats>> = vec![None; n];
    values.iter().enumerate().for_each(|(i, value)| {
        number_stats[*value] = Some(Stats::new(i));
    });
    let mut number: usize = *values.last().unwrap();
    for i in values.len()..n {
        number = number_stats.get(number).unwrap().as_ref().unwrap().next();
        match number_stats.get_mut(number).unwrap() {
            Some(stats) => stats.said(i),
            None => number_stats[number] = Some(Stats::new(i)),
        };
    }
    number
}
