use aoc::{answer, Reader};
use std::cmp::Ordering;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Eq)]
enum Packet {
    Item(usize),
    List(Vec<Packet>),
}

impl FromStr for Packet {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut stack = Vec::default();
        let mut value = String::default();
        for ch in s.chars() {
            match ch {
                '[' => stack.push(Vec::default()),
                '0'..='9' => value.push(ch),
                ',' | ']' => {
                    if !value.is_empty() {
                        let packet = Packet::Item(value.parse().unwrap());
                        stack.last_mut().unwrap().push(packet);
                        value.clear();
                    }
                }
                _ => unreachable!(),
            };
            if ch == ']' {
                let packet = Self::List(stack.pop().unwrap());
                if !stack.is_empty() {
                    stack.last_mut().unwrap().push(packet);
                } else {
                    return Ok(packet);
                }
            }
        }
        unreachable!()
    }
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Self::List(p1), Self::List(p2)) => (0..p1.len().min(p2.len()))
                .map(|i| p1[i].cmp(&p2[i]))
                .find(|&result| result != Ordering::Equal)
                .unwrap_or(p1.len().cmp(&p2.len())),
            (Self::Item(i1), Self::Item(i2)) => i1.cmp(i2),
            (Self::List(_), Self::Item(_)) => self.cmp(&other.wrap()),
            (Self::Item(_), Self::List(_)) => self.wrap().cmp(other),
        }
    }
}

impl PartialOrd for Packet {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Packet {
    fn wrap(&self) -> Self {
        Self::List(vec![self.clone()])
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let packets = Reader::default()
        .lines::<String>()
        .iter()
        .filter(|line| !line.is_empty())
        .map(|line| line.parse().unwrap())
        .collect::<Vec<_>>();
    answer::part1(4809, sum_adjacent(&packets));
    answer::part2(22600, decoder_key(&packets));
}

fn sum_adjacent(packets: &[Packet]) -> usize {
    packets
        .chunks(2)
        .enumerate()
        .map(|(i, pair)| if pair[0] < pair[1] { i + 1 } else { 0 })
        .sum()
}

fn decoder_key(packets: &[Packet]) -> usize {
    (num_less(packets, "[[2]]") + 1) * (num_less(packets, "[[6]]") + 2)
}

fn num_less(packets: &[Packet], value: &str) -> usize {
    let target = value.parse().unwrap();
    packets.iter().filter(|packet| packet < &&target).count()
}
