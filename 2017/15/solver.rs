use aoc_lib::answer;
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Generator {
    value: usize,
    wait: bool,
    factor: usize,
    multiple: usize,
}

impl Generator {
    fn new(value: usize, wait: bool, factor: usize, multiple: usize) -> Self {
        Self {
            value,
            wait,
            factor,
            multiple,
        }
    }

    fn next(&mut self) -> u16 {
        self.calculate();
        while self.wait && self.value % self.multiple != 0 {
            self.calculate();
        }
        self.value as u16
    }

    fn calculate(&mut self) {
        self.value = (self.value * self.factor) % 2_147_483_647;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let starts: Vec<usize> = Reader::default()
        .read_lines()
        .iter()
        .map(|line| line.split(' ').last().unwrap().parse().unwrap())
        .collect();
    answer::part1(592, matches(&starts, 40_000_000, false));
    answer::part2(320, matches(&starts, 5_000_000, true));
}

fn matches(starts: &[usize], n: usize, wait: bool) -> usize {
    let mut a = Generator::new(starts[0], wait, 16_807, 4);
    let mut b = Generator::new(starts[1], wait, 48_271, 8);
    let mut count = 0;
    for _ in 0..n {
        if a.next() == b.next() {
            count += 1;
        }
    }
    count
}
