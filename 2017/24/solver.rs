use aoc_lib::answer;
use aoc_lib::collections::{HashMap, HashSet};
use aoc_lib::reader::Reader;
use std::cmp::Ordering;
use std::collections::VecDeque;

#[derive(Debug, Clone, Default)]
struct Bridge(Vec<(u8, u8)>);

impl Bridge {
    fn last(&self) -> u8 {
        self.0.last().unwrap_or(&(0, 0)).1
    }

    fn contains(&self, start: u8, end: u8) -> bool {
        self.0.contains(&(start, end)) || self.0.contains(&(end, start))
    }

    fn add(&self, start: u8, end: u8) -> Self {
        let mut copied_bridge = self.0.clone();
        copied_bridge.push((start, end));
        Self(copied_bridge)
    }

    fn strength(&self) -> usize {
        self.0
            .iter()
            .map(|(start, end)| (*start as usize) + (*end as usize))
            .sum()
    }

    fn len(&self) -> usize {
        self.0.len()
    }
}

#[derive(Debug, Default)]
struct BridgeData {
    strongest: usize,
    longest: usize,
    longest_strongest: usize,
}

impl BridgeData {
    fn update(&mut self, bridge: &Bridge) {
        let (strength, length) = (bridge.strength(), bridge.len());
        self.strongest = self.strongest.max(strength);
        match length.cmp(&self.longest) {
            Ordering::Greater => {
                self.longest = length;
                self.longest_strongest = strength;
            }
            Ordering::Equal => {
                self.longest_strongest = self.longest_strongest.max(strength);
            }
            Ordering::Less => (),
        };
    }
}

#[derive(Debug)]
struct BridgeBuilder {
    components: HashMap<u8, HashSet<u8>>,
}

impl BridgeBuilder {
    fn new(lines: &[String]) -> Self {
        let mut components: HashMap<u8, HashSet<u8>> = HashMap::default();
        lines.iter().for_each(|line| {
            let (p1, p2) = line.split_once('/').unwrap();
            let v1: u8 = p1.parse().unwrap();
            let v2: u8 = p2.parse().unwrap();
            components.entry(v1).or_default().insert(v2);
            components.entry(v2).or_default().insert(v1);
        });
        Self { components }
    }

    fn build(&self) -> BridgeData {
        let mut data = BridgeData::default();
        let mut q = VecDeque::default();
        q.push_back(Bridge::default());
        while !q.is_empty() {
            let bridge = q.pop_front().unwrap();
            data.update(&bridge);
            let start = bridge.last();
            let ends = &self.components[&start];
            // If there's a duplicate port, i.e. 35/35, choose it as the only
            // option since it adds strength & length without changing the port
            if ends.contains(&start) && !bridge.contains(start, start) {
                q.push_back(bridge.add(start, start));
            } else {
                for end in ends.iter() {
                    if !bridge.contains(start, *end) {
                        q.push_back(bridge.add(start, *end));
                    }
                }
            }
        }
        data
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let data = BridgeBuilder::new(&lines).build();
    answer::part1(1656, data.strongest);
    answer::part2(1642, data.longest_strongest);
}
