use aoc_lib::answer;
use std::collections::VecDeque;

#[derive(Debug)]
struct Lock {
    steps: usize,
    queue: VecDeque<usize>,
}

impl Lock {
    fn new(steps: usize) -> Self {
        Self {
            steps,
            queue: [0].into(),
        }
    }

    fn insert(&mut self, value: usize) {
        let rotations = (self.steps + 1) % self.queue.len();
        self.queue.rotate_left(rotations);
        self.queue.push_front(value);
    }

    fn after(&self, target: usize) -> usize {
        let index = self.queue.iter().position(|&value| value == target);
        self.queue.get(index.unwrap() + 1).unwrap().clone()
    }
}

fn main() {
    answer::part1(996, run_lock(2_017, 2_017));
    answer::part2(1898341, run_lock(50_000_000, 0));
}

fn run_lock(steps: usize, after: usize) -> usize {
    let mut lock = Lock::new(344);
    for i in 1..=steps {
        lock.insert(i);
    }
    lock.after(after)
}