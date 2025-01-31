use aoc::{answer, Reader};
use std::str::FromStr;

#[derive(Debug, Clone)]
struct Disk {
    id: usize,
    positions: usize,
    start: usize,
}

impl FromStr for Disk {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split_whitespace().collect();
        Ok(Self {
            id: parts[1][1..].parse().unwrap(),
            positions: parts[3].parse().unwrap(),
            start: parts[11][..parts[11].len() - 1].parse().unwrap(),
        })
    }
}

impl Disk {
    fn passes(&self, time: usize) -> bool {
        let position = time + self.id + self.start;
        position % self.positions == 0
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let disks: Vec<Disk> = Reader::default().read_from_str();
    answer::part1(121834, calculate(disks.clone(), false));
    answer::part2(3208099, calculate(disks.clone(), true));
}

fn calculate(mut disks: Vec<Disk>, add_disk: bool) -> usize {
    if add_disk {
        disks.push(Disk {
            id: disks.len() + 1,
            positions: 11,
            start: 0,
        });
    }
    (0..)
        .find(|&time| disks.iter().all(|disk| disk.passes(time)))
        .unwrap()
}
