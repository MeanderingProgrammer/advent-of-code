use aoc_lib::answer;
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Generator {
    value: usize,
    wait: bool,
    factor: usize,
    mult: usize,
}

impl Generator {
    fn new(value: usize, wait: bool, factor: usize, mult: usize) -> Self {
        Self {
            value,
            wait,
            factor,
            mult,
        }
    }

    fn next(&mut self) -> u16 {
        self.calculate();
        while self.wait && self.value % self.mult != 0 {
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
    let generators: Vec<usize> = Reader::default()
        .read_lines()
        .iter()
        .map(|line| line.split(' ').last().unwrap().parse().unwrap())
        .collect();
    answer::part1(592, matches(&generators, 40_000_000, false));
    answer::part2(320, matches(&generators, 5_000_000, true));
}

fn matches(generators: &[usize], n: usize, wait: bool) -> usize {
    let mut gen_a = Generator::new(generators[0], wait, 16_807, 4);
    let mut gen_b = Generator::new(generators[1], wait, 48_271, 8);
    let mut count = 0;
    for _ in 0..n {
        if gen_a.next() == gen_b.next() {
            count += 1;
        }
    }
    count
}
