use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Cups {
    current: usize,
    low: usize,
    high: usize,
    cups: Vec<usize>,
}

impl Cups {
    fn new(values: Vec<usize>) -> Self {
        let mut cups = vec![0; values.len() + 1];
        for i in 0..values.len() - 1 {
            cups[values[i]] = values[i + 1];
        }
        cups[values[values.len() - 1]] = values[0];
        Self {
            current: values[0],
            low: *values.iter().min().unwrap(),
            high: *values.iter().max().unwrap(),
            cups,
        }
    }

    fn run(&mut self) {
        let mut aside: Vec<usize> = vec![self.cups[self.current]];
        aside.push(self.cups[aside[0]]);
        aside.push(self.cups[aside[1]]);
        let destination = self.get_destination(&aside);
        self.cups[self.current] = self.cups[aside[2]];
        self.cups[aside[2]] = self.cups[destination];
        self.cups[destination] = aside[0];
        self.current = self.cups[self.current];
    }

    fn get_destination(&self, aside: &Vec<usize>) -> usize {
        let mut destination = self.previous(self.current);
        while aside.contains(&destination) {
            destination = self.previous(destination);
        }
        destination
    }

    fn previous(&self, value: usize) -> usize {
        if value - 1 < self.low {
            self.high
        } else {
            value - 1
        }
    }

    fn part_1(&self) -> String {
        let mut result = "".to_string();
        let mut value = self.cups[1];
        while value != 1 {
            result += &value.to_string();
            value = self.cups[value];
        }
        result
    }

    fn part_2(&self) -> usize {
        self.cups[1] * self.cups[self.cups[1]]
    }
}

fn main() {
    answer::part1("45798623", &run(0, 100).part_1());
    answer::part2(235551949822, run(1_000_000, 10_000_000).part_2());
}

fn run(num_cups: usize, rounds: usize) -> Cups {
    let mut values: Vec<usize> = reader::read_chars()
        .iter()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect();
    for i in values.iter().max().unwrap() + 1..=num_cups {
        values.push(i);
    }
    let mut cups = Cups::new(values);
    for _ in 0..rounds {
        cups.run();
    }
    cups
}
