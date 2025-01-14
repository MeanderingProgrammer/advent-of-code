use aoc_lib::answer;
use aoc_lib::bit_set::BitSet;
use aoc_lib::ids::Base;
use aoc_lib::queue::{HeapVariant, PriorityQueue};
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use itertools::Itertools;
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
struct IndividualState {
    location: u8,
    time_left: u16,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct FullState {
    individuals: Vec<IndividualState>,
    opened: BitSet,
}

impl FullState {
    fn new(time: u16, individuals: usize) -> Self {
        Self {
            individuals: vec![
                IndividualState {
                    location: 0,
                    time_left: time,
                };
                individuals
            ],
            opened: BitSet::default(),
        }
    }
}

/// Valves are represented using u8s rather than strings
#[derive(Debug)]
struct Cave {
    /// Mapping from each valve to each reachable valve and the time it takes to reach it
    graph: FxHashMap<u8, Vec<(u8, u16)>>,
    /// Mapping from each valve to its flow rate
    valve_flow: FxHashMap<u8, u16>,
}

impl Cave {
    fn traverse(&self, time: u16, individuals: usize) -> u16 {
        let mut queue = PriorityQueue::new(HeapVariant::Max);
        queue.push(FullState::new(time, individuals), 0);
        let mut max_score: u16 = 0;
        while !queue.is_empty() {
            let (state, score) = queue.pop().unwrap();
            if score + self.max_score(&state, 3) < max_score {
                continue;
            }
            max_score = max_score.max(score);
            let next_states = match individuals {
                1 => self.next_options(&state, score, 0),
                2 => {
                    let states_1 = self.next_options(&state, score, 0);
                    let states_2 = self.next_options(&state, score, 1);
                    if states_1.is_empty() {
                        states_2
                    } else if states_2.is_empty() {
                        states_1
                    } else {
                        let mut result = vec![];
                        for (next_state, next_score) in states_1.into_iter() {
                            let mut followup_states = self.next_options(&next_state, next_score, 1);
                            if followup_states.is_empty() {
                                result.push((next_state, next_score));
                            } else {
                                result.append(&mut followup_states);
                            }
                        }
                        result
                    }
                }
                _ => unreachable!(),
            };
            for (next_state, next_score) in next_states {
                queue.push(next_state, next_score);
            }
        }
        max_score
    }

    fn next_options(&self, state: &FullState, score: u16, i: usize) -> Vec<(FullState, u16)> {
        let individual = &state.individuals[i];
        self.graph[&individual.location]
            .iter()
            .filter(|(_, time)| individual.time_left > *time)
            .filter(|(destination, _)| !state.opened.contains(*destination))
            .map(|(destination, time)| {
                let time_left = individual.time_left - time - 1;
                let mut individuals = state.individuals.clone();
                individuals[i] = IndividualState {
                    location: *destination,
                    time_left,
                };
                let mut opened = state.opened.clone();
                opened.add(*destination);
                let next_state = FullState {
                    individuals,
                    opened,
                };
                let next_score = score + (self.valve_flow[destination] * time_left);
                (next_state, next_score)
            })
            .collect()
    }

    fn max_score(&self, state: &FullState, move_time: u16) -> u16 {
        let mut highest_values = self
            .valve_flow
            .iter()
            .filter(|(name, _)| !state.opened.contains(**name))
            .map(|(_, &flow_rate)| flow_rate)
            .sorted()
            .rev()
            .peekable();

        let mut times_left: Vec<u16> = state
            .individuals
            .iter()
            .map(|individual| individual.time_left)
            .collect();

        let mut additional_score = 0;
        while times_left.iter().max().unwrap() > &move_time && highest_values.peek().is_some() {
            let index_of_max = times_left
                .iter()
                .enumerate()
                .max_by(|(_, a), (_, b)| a.cmp(b))
                .map(|(index, _)| index)
                .unwrap();

            times_left[index_of_max] -= move_time;
            additional_score += times_left[index_of_max] * highest_values.next().unwrap();
        }
        additional_score
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let valves = Reader::default().read_from_str();
    let cave = create_cave(valves, Valve::index("AA"));
    answer::part1(1873, cave.traverse(30, 1));
    answer::part2(2425, cave.traverse(26, 2));
}

fn create_cave(valves: Vec<Valve>, start: u32) -> Cave {
    let distances = floyd_warshall(&valves);

    let ordered: Vec<u32> = valves
        .iter()
        .filter(|valve| valve.name == start || valve.flow_rate > 0)
        .map(|valve| valve.name)
        .sorted()
        .collect();

    let valve_flow: FxHashMap<u8, u16> = valves
        .iter()
        .map(|valve| (valve, ordered.iter().position(|v| v == &valve.name)))
        .filter(|(_, index)| index.is_some())
        .map(|(valve, index)| (index.unwrap() as u8, valve.flow_rate))
        .collect();

    let mut graph: FxHashMap<u8, Vec<(u8, u16)>> = FxHashMap::default();
    (0..ordered.len())
        .flat_map(|v1| (1..ordered.len()).map(move |v2| (v1, v2)))
        .filter(|(v1, v2)| v1 != v2)
        .for_each(|(v1, v2)| {
            let weight = distances.get(&(ordered[v1], ordered[v2])).unwrap();
            graph.entry(v1 as u8).or_default().push((v2 as u8, *weight));
        });

    Cave { graph, valve_flow }
}

fn floyd_warshall(valves: &[Valve]) -> FxHashMap<(u32, u32), u16> {
    let mut dist = FxHashMap::default();
    for v1 in valves.iter() {
        for v2 in valves.iter() {
            dist.insert((v1.name, v2.name), u16::MAX);
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
