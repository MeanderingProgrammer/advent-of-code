use aoc::{answer, Reader};

#[derive(Debug)]
struct LockIndex {
    step: usize,
    current: usize,
}

impl LockIndex {
    fn new(step: usize) -> Self {
        Self {
            step: step + 1,
            current: 0,
        }
    }

    fn skip(&mut self, length: usize, n: usize) {
        self.current = (self.current + self.step * n) % length;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let step_size = Reader::default().read_int()[0] as usize;
    answer::part1(996, after_last(step_size, 2_017));
    answer::part2(1898341, after_zero(step_size, 50_000_000));
}

fn after_last(step: usize, steps: usize) -> usize {
    let mut index = LockIndex::new(step);
    let mut values = vec![0];
    for i in 1..=steps {
        index.skip(i, 1);
        values.insert(index.current, i);
    }
    values[index.current + 1]
}

fn after_zero(step: usize, steps: usize) -> usize {
    let mut index = LockIndex::new(step);
    let mut result = 0;
    let mut n = 1;
    while n <= steps {
        if index.current == 0 {
            result = n;
        }
        let skip = (n - index.current).div_ceil(step);
        n += skip;
        index.skip(n, skip);
    }
    result
}
