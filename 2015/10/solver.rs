use aoc::prelude::*;

#[derive(Debug)]
struct Game {
    value: Vec<u8>,
}

impl Game {
    fn play(&mut self, n: usize) -> usize {
        for _ in 0..n {
            self.play_round();
        }
        self.value.len()
    }

    fn play_round(&mut self) {
        let mut next_value: Vec<u8> = Vec::default();
        for i in 0..self.value.len() {
            if i > 0 && self.value[i] == self.value[i - 1] {
                let last_index = next_value.len() - 1;
                next_value[last_index - 1] += 1;
            } else {
                next_value.push(1);
                next_value.push(self.value[i]);
            }
        }
        self.value = next_value;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let value = Reader::default().chars();
    let mut game = Game { value };
    answer::part1(360154, game.play(40));
    answer::part2(5103798, game.play(10));
}
