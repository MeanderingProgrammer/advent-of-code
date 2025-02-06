use aoc::{answer, Reader};

#[derive(Debug)]
struct Transformer {
    subject: i64,
}

impl Transformer {
    fn new(subject: i64) -> Self {
        Self { subject }
    }

    fn loop_size(&self, goal: i64) -> i64 {
        let mut result = 0;
        let mut value = 1;
        while value != goal {
            result += 1;
            value = self.next_value(value);
        }
        result
    }

    fn run(&self, loops: i64) -> i64 {
        let mut value = 1;
        (0..loops).for_each(|_| value = self.next_value(value));
        value
    }

    fn next_value(&self, value: i64) -> i64 {
        (value * self.subject) % 20201227
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().lines();
    let (card, door) = (data[0], data[1]);
    let loop_size = Transformer::new(7).loop_size(card);
    answer::part1(3015200, Transformer::new(door).run(loop_size));
}
