use aoc_lib::answer;
use aoc_lib::bit_set::BitSet;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use itertools::Itertools;
use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{alpha0, digit0},
    combinator::map_res,
    multi::separated_list0,
    sequence::tuple,
    IResult,
};
use petgraph::{algo::floyd_warshall::floyd_warshall, graphmap::DiGraphMap};
use priority_queue::PriorityQueue;

#[derive(Debug)]
struct Valve {
    name: String,
    flow_rate: u16,
    leads_to: Vec<String>,
}

impl Valve {
    fn from_str(input: &str) -> IResult<&str, Self> {
        // Valve OM has flow rate=0; tunnels lead to valves AA, EZ
        let (input, name) = tuple((tag("Valve "), alpha0))(input)?;
        let (input, flow_rate) = tuple((
            tag(" has flow rate="),
            map_res(digit0, |s: &str| s.parse()),
            tag("; "),
        ))(input)?;
        let (input, _) = alt((
            tag("tunnel leads to valve "),
            tag("tunnels lead to valves "),
        ))(input)?;
        let (input, valves) = separated_list0(tag(", "), alpha0)(input)?;
        Ok((
            input,
            Self {
                name: name.1.to_string(),
                flow_rate: flow_rate.1,
                leads_to: valves.iter().map(|valve| valve.to_string()).collect(),
            },
        ))
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
        let mut queue = PriorityQueue::new();
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
                _ => panic!("Failure"),
            };
            for (next_state, next_score) in next_states {
                queue.push_increase(next_state, next_score);
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
    let valves = Reader::default().read(|line| Valve::from_str(line).unwrap().1);
    let cave = create_cave(valves, "AA");
    answer::part1(1873, cave.traverse(30, 1));
    answer::part2(2425, cave.traverse(26, 2));
}

fn create_cave(valves: Vec<Valve>, start: &str) -> Cave {
    let distance_graph = DiGraphMap::from_edges(valves.iter().flat_map(|valve| {
        let start = &valve.name;
        let ends = &valve.leads_to;
        ends.iter().map(|end| (start.as_str(), end.as_str(), ()))
    }));
    let distances = floyd_warshall(&distance_graph, |_| 1).unwrap();

    let ordered: Vec<String> = valves
        .iter()
        .filter(|valve| valve.name == start || valve.flow_rate > 0)
        .map(|valve| valve.name.to_string())
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
            let weight = distances.get(&(&ordered[v1], &ordered[v2])).unwrap();
            graph.entry(v1 as u8).or_default().push((v2 as u8, *weight));
        });

    Cave { graph, valve_flow }
}
