use aoc_lib::answer;

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
        let to_compare: Vec<u8> = self
            .scores
            .iter()
            .rev()
            .skip(offset)
            .take(self.digits.len())
            .rev()
            .map(|value| *value)
            .collect();
        to_compare == self.digits
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
    let goal: usize = 170_641;
    let mut recipes = Recipes::new(goal);
    let sequence = recipes.evolve();
    answer::part1("2103141159", &sequence[goal..goal + 10]);
    answer::part2(20165733, sequence.find(&goal.to_string()).unwrap());
}
