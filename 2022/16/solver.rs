use aoc_lib::answer;
use aoc_lib::bit_set::BitSet;
use aoc_lib::collections::HashMap;
use aoc_lib::ids::Base;
use aoc_lib::iter::Iter;
use aoc_lib::queue::{HeapKind, PriorityQueue};
use aoc_lib::reader::Reader;
use std::str::FromStr;

#[derive(Debug)]
struct Valve {
    name: u32,
    flow_rate: u16,
    leads_to: Vec<u32>,
}

impl FromStr for Valve {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Valve OM has flow rate=0; tunnels lead to valves AA, EZ
        let (valve_rate, tunnels) = s.split_once("; ").unwrap();
        let name = valve_rate.split_whitespace().nth(1).unwrap();
        let (_, flow_rate) = valve_rate.split_once('=').unwrap();
        let plural = tunnels.split_whitespace().next().unwrap() == "tunnels";
        let delim = if plural { "valves " } else { "valve " };
        let (_, tunnels) = tunnels.split_once(delim).unwrap();
        Ok(Self {
            name: Self::index(name),
            flow_rate: flow_rate.parse().unwrap(),
            leads_to: tunnels.split(", ").map(Self::index).collect(),
        })
    }
}

impl Valve {
    fn index(name: &str) -> u32 {
        Base::str_insensitive(name)
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Individual {
    location: u8,
    time: u8,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct FullState<const N: usize> {
    individuals: [Individual; N],
    opened: BitSet,
}

impl<const N: usize> FullState<N> {
    fn new(time: u8) -> Self {
        Self {
            individuals: std::array::from_fn(|_| Individual { location: 0, time }),
            opened: BitSet::default(),
        }
    }

    fn next(&self, cave: &Cave) -> Vec<(Self, u16)> {
        match N {
            1 => self.next_1(cave),
            2 => self.next_2(cave),
            _ => unreachable!(),
        }
    }

    fn next_1(&self, cave: &Cave) -> Vec<(Self, u16)> {
        self.individual(cave, 0)
    }

    fn next_2(&self, cave: &Cave) -> Vec<(Self, u16)> {
        let states = self.individual(cave, 0);
        if states.is_empty() {
            self.individual(cave, 1)
        } else {
            let mut result = Vec::default();
            for (state, score) in states {
                let states_2 = state.individual(cave, 1);
                if states_2.is_empty() {
                    result.push((state, score));
                } else {
                    for (state_2, score_2) in states_2 {
                        result.push((state_2, score + score_2));
                    }
                }
            }
            result
        }
    }

    fn individual(&self, cave: &Cave, i: usize) -> Vec<(Self, u16)> {
        let individual = &self.individuals[i];
        cave.graph[&individual.location]
            .iter()
            .filter(|(_, time)| individual.time > *time)
            .filter(|(destination, _)| !self.opened.contains(*destination))
            .map(|(destination, time)| {
                let time = individual.time - time - 1;
                let state = self.apply(i, *destination, time);
                let score = cave.flows[destination] * time as u16;
                (state, score)
            })
            .collect()
    }

    fn apply(&self, i: usize, location: u8, time: u8) -> Self {
        let mut individuals = self.individuals.clone();
        individuals[i] = Individual { location, time };
        Self {
            individuals,
            opened: self.opened.extend([location]),
        }
    }

    fn possible(&self, cave: &Cave, takes: u8) -> u16 {
        let flows = cave
            .flows
            .iter()
            .filter(|(name, _)| !self.opened.contains(**name))
            .map(|(_, flow)| flow)
            .sorted()
            .rev();

        let mut times: Vec<u8> = self
            .individuals
            .iter()
            .map(|individual| individual.time)
            .collect();

        let mut result = 0;
        for flow in flows {
            let (index, _) = times
                .iter()
                .enumerate()
                .max_by(|(_, a), (_, b)| a.cmp(b))
                .unwrap();
            if times[index] <= takes {
                break;
            }
            times[index] -= takes;
            result += times[index] as u16 * flow;
        }
        result
    }
}

#[derive(Debug)]
struct Cave {
    // Mapping from valve to each reachable valve and the time it takes to reach it
    graph: HashMap<u8, Vec<(u8, u8)>>,
    // Mapping from each valve to its flow rate
    flows: HashMap<u8, u16>,
}

impl Cave {
    fn traverse<const N: usize>(&self, time: u8) -> u16 {
        let mut queue = PriorityQueue::new(HeapKind::Max);
        queue.push(FullState::<N>::new(time), 0);
        let mut max_score: u16 = 0;
        while let Some((state, score)) = queue.pop() {
            if score + state.possible(self, 3) > max_score {
                max_score = max_score.max(score);
                let next_states = state.next(self);
                for (next_state, next_score) in next_states {
                    queue.push(next_state, score + next_score);
                }
            }
        }
        max_score
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let valves = Reader::default().read_from_str();
    let cave = create_cave(valves, Valve::index("AA"));
    answer::part1(1873, cave.traverse::<1>(30));
    answer::part2(2425, cave.traverse::<2>(26));
}

fn create_cave(valves: Vec<Valve>, start: u32) -> Cave {
    let distances = floyd_warshall(&valves);

    let ordered: Vec<u32> = valves
        .iter()
        .filter(|valve| valve.name == start || valve.flow_rate > 0)
        .map(|valve| valve.name)
        .sorted()
        .collect();

    let flows: HashMap<u8, u16> = valves
        .iter()
        .map(|valve| (valve, ordered.iter().position(|v| v == &valve.name)))
        .filter(|(_, index)| index.is_some())
        .map(|(valve, index)| (index.unwrap() as u8, valve.flow_rate))
        .collect();

    let mut graph: HashMap<u8, Vec<(u8, u8)>> = HashMap::default();
    (0..ordered.len())
        .flat_map(|v1| (1..ordered.len()).map(move |v2| (v1, v2)))
        .filter(|(v1, v2)| v1 != v2)
        .for_each(|(v1, v2)| {
            let weight = distances.get(&(ordered[v1], ordered[v2])).unwrap();
            graph.entry(v1 as u8).or_default().push((v2 as u8, *weight));
        });

    Cave { graph, flows }
}

fn floyd_warshall(valves: &[Valve]) -> HashMap<(u32, u32), u8> {
    let mut dist = HashMap::default();
    for v1 in valves.iter() {
        for v2 in valves.iter() {
            dist.insert((v1.name, v2.name), u8::MAX);
        }
    }
    for v in valves.iter() {
        dist.insert((v.name, v.name), 0);
    }
    for v in valves.iter() {
        for e in v.leads_to.iter() {
            dist.insert((v.name, *e), 1);
        }
    }
    for k in valves.iter() {
        for i in valves.iter() {
            for j in valves.iter() {
                let ik = *dist.get(&(i.name, k.name)).unwrap();
                let kj = *dist.get(&(k.name, j.name)).unwrap();
                let ij = *dist.get(&(i.name, j.name)).unwrap();
                let (result, overflow) = ik.overflowing_add(kj);
                if !overflow && ij > result {
                    dist.insert((i.name, j.name), result);
                }
            }
        }
    }
    dist
}
