use aoc::{answer, Reader};

#[derive(Debug)]
struct Recipes {
    e1: usize,
    e2: usize,
    scores: Vec<u8>,
    goal: Vec<u8>,
}

impl Recipes {
    fn new(goal: &str) -> Self {
        Self {
            e1: 0,
            e2: 1,
            scores: vec![3, 7],
            goal: goal
                .chars()
                .map(|ch| ch.to_digit(10).unwrap() as u8)
                .collect(),
        }
    }

    fn evolve(&mut self) {
        while !self.step() {}
    }

    fn step(&mut self) -> bool {
        let total = self.scores[self.e1] + self.scores[self.e2];
        if (total >= 10 && self.append(1)) || self.append(total % 10) {
            true
        } else {
            self.e1 = self.next(self.e1);
            self.e2 = self.next(self.e2);
            false
        }
    }

    fn append(&mut self, score: u8) -> bool {
        self.scores.push(score);
        let (scores, goal) = (self.scores.len(), self.goal.len());
        scores >= goal && self.goal == self.scores[scores - goal..]
    }

    fn next(&self, current: usize) -> usize {
        let (score, scores) = (self.scores[current] as usize, self.scores.len());
        let result = current + score + 1;
        if result >= scores {
            result % scores
        } else {
            result
        }
    }

    fn part1(&self, start: usize) -> String {
        self.scores
            .iter()
            .skip(start)
            .take(10)
            .map(|score| score.to_string())
            .collect()
    }

    fn part2(&self) -> usize {
        self.scores.len() - self.goal.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let goal = Reader::default().read_line();
    let mut recipes = Recipes::new(&goal);
    recipes.evolve();
    answer::part1("2103141159", &recipes.part1(goal.parse().unwrap()));
    answer::part2(20165733, recipes.part2());
}
