use aoc_lib::answer;

#[derive(Debug)]
struct Generator {
    value: u64,
    factor: u64,
    mult: u64,
}

impl Generator {
    fn new(value: u64, factor: u64, mult: u64) -> Self {
        Self {
            value,
            factor,
            mult,
        }
    }

    fn next(&mut self, wait_mult: bool) -> u64 {
        self.calculate();
        while wait_mult && self.value % self.mult != 0 {
            self.calculate();
        }
        self.value
    }

    fn calculate(&mut self) {
        self.value *= self.factor;
        self.value %= 2_147_483_647;
    }
}

fn main() {
    answer::part1(592, matches(40_000_000, false));
    answer::part2(320, matches(5_000_000, true));
}

fn matches(n: i64, wait_mult: bool) -> u64 {
    let mut gen_a = Generator::new(277, 16_807, 4);
    let mut gen_b = Generator::new(349, 48_271, 8);
    let mut count = 0;
    for _ in 0..n {
        if equal(gen_a.next(wait_mult), gen_b.next(wait_mult)) {
            count += 1;
        }
    }
    count
}

fn equal(v1: u64, v2: u64) -> bool {
    v1 as u16 == v2 as u16
}
