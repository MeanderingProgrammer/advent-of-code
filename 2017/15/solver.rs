use aoc::{answer, Parser, Reader};
use rayon::prelude::*;

#[derive(Debug)]
struct Gen {
    value: usize,
    factor: usize,
}

impl Gen {
    fn compute(&mut self, multiple: u16) -> (Vec<u16>, Vec<u16>) {
        let (n, m) = (40_000_000, 5_000_000);
        let (mut vals, mut mods) = (Vec::with_capacity(n), Vec::with_capacity(m));
        while !Self::full(&vals) || !Self::full(&mods) {
            let value = self.next();
            if !Self::full(&vals) {
                vals.push(value);
            }
            if !Self::full(&mods) && value % multiple == 0 {
                mods.push(value);
            }
        }
        (vals, mods)
    }

    fn next(&mut self) -> u16 {
        self.value *= self.factor;
        self.value %= 2_147_483_647;
        self.value as u16
    }

    fn full(values: &Vec<u16>) -> bool {
        values.len() == values.capacity()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines: Vec<String> = Reader::default().lines();
    let [a] = Parser::values(&lines[0], " ").unwrap();
    let [b] = Parser::values(&lines[1], " ").unwrap();
    let generators = [(a, 16_807, 4), (b, 48_271, 8)];
    let values: Vec<(Vec<u16>, Vec<u16>)> = generators
        .into_par_iter()
        .map(|(value, factor, multiple)| Gen { value, factor }.compute(multiple))
        .collect();
    let (a, b) = (&values[0], &values[1]);
    answer::part1(592, matches(&a.0, &b.0));
    answer::part2(320, matches(&a.1, &b.1));
}

fn matches(a: &[u16], b: &[u16]) -> usize {
    assert_eq!(a.len(), b.len());
    std::iter::zip(a, b).filter(|(a, b)| a == b).count()
}
