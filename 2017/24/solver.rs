use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::cmp::Ordering;

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
    components: FxHashMap<u8, Vec<u8>>,
}

impl BridgeBuilder {
    fn build(&self) -> BridgeData {
        let mut data = BridgeData::default();
        self.generate(&mut data, Bridge::default());
        data
    }

    fn generate(&self, data: &mut BridgeData, bridge: Bridge) {
        data.update(&bridge);
        let start = bridge.last();
        for end in self.components[&start].iter() {
            if !bridge.contains(start, *end) {
                self.generate(data, bridge.add(start, *end));
            }
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = get_bridge_builder().build();
    answer::part1(1656, data.strongest);
    answer::part2(1642, data.longest_strongest);
}

fn get_bridge_builder() -> BridgeBuilder {
    let mut components: FxHashMap<u8, Vec<u8>> = FxHashMap::default();
    Reader::default().read_lines().iter().for_each(|line| {
        let (p1, p2) = line.split_once('/').unwrap();
        let v1: u8 = p1.parse().unwrap();
        let v2: u8 = p2.parse().unwrap();
        components.entry(v1).or_default().push(v2);
        components.entry(v2).or_default().push(v1);
    });
    BridgeBuilder { components }
}
