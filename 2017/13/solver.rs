use aoc::{answer, Reader, Str};
use std::str::FromStr;

#[derive(Debug)]
struct Scanner {
    layer: usize,
    layer_range: usize,
    roundtrip: usize,
}

impl FromStr for Scanner {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let [layer, layer_range] = [0, 1].map(|i| Str::nth(s, ':', i));
        Ok(Self::new(layer, layer_range))
    }
}

impl Scanner {
    fn new(layer: usize, layer_range: usize) -> Self {
        Self {
            layer,
            layer_range,
            roundtrip: (layer_range - 1) * 2,
        }
    }

    fn caught(&self, offset: usize) -> bool {
        (self.layer + offset) % self.roundtrip == 0
    }

    fn severity(&self) -> usize {
        self.layer * self.layer_range
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let scanners = Reader::default().lines();
    answer::part1(632, trip_severity(&scanners));
    answer::part2(3849742, find_wait(&scanners));
}

fn trip_severity(scanners: &[Scanner]) -> usize {
    scanners
        .iter()
        .filter(|scanner| scanner.caught(0))
        .map(|scanner| scanner.severity())
        .sum()
}

fn find_wait(scanners: &[Scanner]) -> usize {
    (0..)
        .find(|&offset| !scanners.iter().any(|scanner| scanner.caught(offset)))
        .unwrap()
}
