use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct LockIndex {
    step_size: usize,
    current: usize,
}

impl LockIndex {
    fn new(step_size: usize, current: usize) -> Self {
        Self { step_size, current }
    }

    fn next(&mut self, length: usize) -> usize {
        self.current = ((self.current + self.step_size) % length) + 1;
        self.current
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let step_size = reader::read_int()[0] as usize;
    answer::part1(996, after_last(step_size, 2_017));
    answer::part2(1898341, after_zero(step_size, 50_000_000));
}

fn after_last(step_size: usize, steps: usize) -> usize {
    let mut values = vec![0];
    let mut index = LockIndex::new(step_size, 0);
    for i in 1..=steps {
        values.insert(index.next(i), i);
    }
    values[index.current + 1]
}

fn after_zero(step_size: usize, steps: usize) -> usize {
    let mut result = 0;
    let mut index = LockIndex::new(step_size, 0);
    for i in 1..=steps {
        if index.next(i) == 1 {
            result = i;
        }
    }
    result
}
