use aoc_lib::answer;
use aoc_lib::reader::Reader;
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
        let (layer, layer_range) = s.split_once(": ").unwrap();
        Ok(Self::new(
            layer.parse().unwrap(),
            layer_range.parse().unwrap(),
        ))
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
    let scanners: Vec<Scanner> = Reader::default().read(|line| line.parse().unwrap());
    answer::part1(632, trip_severity(&scanners));
    answer::part2(3849742, find_wait(&scanners));
}

fn trip_severity(scanners: &Vec<Scanner>) -> usize {
    scanners
        .iter()
        .filter(|scanner| scanner.caught(0))
        .map(|scanner| scanner.severity())
        .sum()
}

fn find_wait(scanners: &Vec<Scanner>) -> usize {
    (0..)
        .filter(|&offset| !scanners.iter().any(|scanner| scanner.caught(offset)))
        .next()
        .unwrap()
}
