use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Recipes {
    scores: Vec<u8>,
    elf_1: usize,
    elf_2: usize,
    digits: Vec<u8>,
}

impl Recipes {
    fn new(goal: usize) -> Self {
        let digits = goal
            .to_string()
            .chars()
            .map(|ch| ch.to_digit(10).unwrap() as u8)
            .collect();
        Self {
            scores: vec![3, 7],
            elf_1: 0,
            elf_2: 1,
            digits,
        }
    }

    fn evolve(&mut self) -> String {
        while !self.found(0) && !self.found(1) {
            self.step();
        }
        self.scores.iter().map(|score| score.to_string()).collect()
    }

    fn found(&self, offset: usize) -> bool {
        let num_scores = self.scores.len();
        let num_digits = self.digits.len();
        if num_scores < num_digits + offset {
            false
        } else {
            self.digits == &self.scores[num_scores - num_digits - offset..num_scores - offset]
        }
    }

    fn step(&mut self) {
        let total = self.scores[self.elf_1] + self.scores[self.elf_2];
        if total >= 10 {
            self.scores.push(1);
        }
        self.scores.push(total % 10);
        self.elf_1 = self.new_position(self.elf_1);
        self.elf_2 = self.new_position(self.elf_2);
    }

    fn new_position(&self, position: usize) -> usize {
        let score = self.scores[position] as usize;
        (position + score + 1) % self.scores.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let goal = reader::read_int()[0] as usize;
    let mut recipes = Recipes::new(goal);
    let sequence = recipes.evolve();
    answer::part1("2103141159", &sequence[goal..goal + 10]);
    answer::part2(20165733, sequence.find(&goal.to_string()).unwrap());
}
