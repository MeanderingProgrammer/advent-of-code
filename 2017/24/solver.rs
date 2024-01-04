use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug, Clone)]
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

#[derive(Debug)]
struct BridgeBuilder {
    components: HashMap<u8, Vec<u8>>,
}

impl BridgeBuilder {
    fn build(&self) -> Vec<Bridge> {
        let bridge = Bridge(Vec::new());
        self.generate(bridge)
    }

    fn generate(&self, bridge: Bridge) -> Vec<Bridge> {
        let start = bridge.last();
        let mut result: Vec<Bridge> = Vec::new();
        for end in self.components[&start].iter() {
            if !bridge.contains(start, *end) {
                let new_bridge = bridge.add(start, *end);
                result.push(new_bridge.clone());
                result.append(&mut self.generate(new_bridge));
            }
        }
        result
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut components: HashMap<u8, Vec<u8>> = HashMap::new();
    reader::read_lines().iter().for_each(|line| {
        let (p1, p2) = line.split_once("/").unwrap();
        let v1: u8 = p1.parse().unwrap();
        let v2: u8 = p2.parse().unwrap();
        if !components.contains_key(&v1) {
            components.insert(v1, Vec::new());
        }
        components.get_mut(&v1).unwrap().push(v2);
        if !components.contains_key(&v2) {
            components.insert(v2, Vec::new());
        }
        components.get_mut(&v2).unwrap().push(v1);
    });
    let bridge_builder = BridgeBuilder { components };
    let bridges = bridge_builder.build();
    answer::part1(1656, strongest(&bridges));
    answer::part2(1642, longest_strongest(&bridges));
}

fn strongest(bridges: &Vec<Bridge>) -> usize {
    bridges
        .iter()
        .map(|bridge| bridge.strength())
        .max()
        .unwrap()
}

fn longest_strongest(bridges: &Vec<Bridge>) -> usize {
    let longest = bridges.iter().map(|bridge| bridge.len()).max().unwrap();
    let all_longest = bridges
        .iter()
        .filter(|bridge| bridge.len() == longest)
        .map(|bridge| bridge.clone())
        .collect();
    strongest(&all_longest)
}
