use aoc_lib::answer;
use aoc_lib::reader;
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
use std::collections::{BTreeSet, HashMap};

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct IndividualState {
    location: String,
    minutes_left: u16,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct FullState {
    individuals: Vec<IndividualState>,
    valves_opened: BTreeSet<String>,
}

impl FullState {
    fn new(starting_time: u16, individuals: usize) -> Self {
        Self {
            individuals: vec![
                IndividualState {
                    location: "AA".to_string(),
                    minutes_left: starting_time,
                };
                individuals
            ],
            valves_opened: ["AA".to_string()].into(),
        }
    }
}

#[derive(Debug)]
struct Cave {
    graph: HashMap<String, Vec<(String, u16)>>,
    valve_to_flow: HashMap<String, u16>,
}

impl Cave {
    fn traverse(&self, starting_time: u16, individuals: usize) -> u16 {
        let mut queue = PriorityQueue::new();
        queue.push(FullState::new(starting_time, individuals), 0);
        let mut max_score: u16 = 0;
        while !queue.is_empty() {
            let (state, score) = queue.pop().unwrap();
            if score + self.max_score(&state) < max_score {
                continue;
            }
            max_score = max_score.max(score);
            let next_states = match individuals {
                1 => self.next_options(&state, score, 0),
                2 => {
                    let first_states = self.next_options(&state, score, 0);
                    let second_states = self.next_options(&state, score, 1);
                    if first_states.is_empty() {
                        second_states
                    } else if second_states.is_empty() {
                        first_states
                    } else {
                        let mut result = vec![];
                        for (next_state, next_score) in first_states.into_iter() {
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
            .filter(|(_, time)| individual.minutes_left > *time)
            .filter(|(destination, _)| !state.valves_opened.contains(destination))
            .map(|(destination, time)| {
                let minutes_left = individual.minutes_left - time - 1;

                let mut valves_opened = state.valves_opened.clone();
                valves_opened.insert(destination.to_string());

                let mut individuals = state.individuals.clone();
                individuals[i] = IndividualState {
                    location: destination.to_string(),
                    minutes_left,
                };

                (
                    FullState {
                        individuals,
                        valves_opened,
                    },
                    score + (self.valve_to_flow[destination] * minutes_left),
                )
            })
            .collect()
    }

    fn max_score(&self, state: &FullState) -> u16 {
        let mut unopened: Vec<u16> = self
            .valve_to_flow
            .iter()
            .filter(|(&ref name, _)| !state.valves_opened.contains(name))
            .map(|(_, &flow_rate)| flow_rate)
            .collect();
        unopened.sort();
        unopened.reverse();

        let mut highest_values = unopened.iter().peekable();

        let mut times_left: Vec<u16> = state
            .individuals
            .iter()
            .map(|individual| individual.minutes_left)
            .collect();

        let mut additional_score = 0;
        while times_left.iter().max().unwrap() > &2 && !highest_values.peek().is_none() {
            let index_of_max = times_left
                .iter()
                .enumerate()
                .max_by(|(_, a), (_, b)| a.cmp(b))
                .map(|(index, _)| index)
                .unwrap();

            times_left[index_of_max] -= 2;
            additional_score += times_left[index_of_max] * highest_values.next().unwrap();
        }
        additional_score
    }
}

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

fn main() {
    let valves = reader::read(|line| Valve::from_str(line).unwrap().1);
    let cave = create_cave(&valves);
    answer::part1(1873, cave.traverse(30, 1));
    answer::part2(2425, cave.traverse(26, 2));
}

fn create_cave(valves: &Vec<Valve>) -> Cave {
    let valve_to_flow = get_valve_to_flow(valves);
    // First create a graph where all edges are weighted at 1
    let mut base_graph: DiGraphMap<&str, ()> = DiGraphMap::new();
    valves.iter().for_each(|valve| {
        valve.leads_to.iter().for_each(|destination| {
            base_graph.add_edge(&valve.name, destination, ());
        });
    });
    // Use a fast algorithm to get distances between all pairs
    let all_distances = floyd_warshall(&base_graph, |_| 1).unwrap();
    // Create a graph weighted by distance for all important valves
    let mut graph: HashMap<String, Vec<(String, u16)>> = HashMap::new();
    for v1 in valve_to_flow.keys() {
        for v2 in valve_to_flow.keys() {
            if v1 != v2 {
                if !graph.contains_key(v1) {
                    graph.insert(v1.to_string(), Vec::new());
                }
                let weight = all_distances.get(&(v1, v2)).unwrap();
                graph.get_mut(v1).unwrap().push((v2.to_string(), *weight));
            }
        }
    }
    Cave {
        graph,
        valve_to_flow,
    }
}

fn get_valve_to_flow(valves: &Vec<Valve>) -> HashMap<String, u16> {
    let mut valve_to_flow = HashMap::new();
    valves
        .iter()
        // Only some of the valves actually matter, in particular the ones with some flow rate + start
        .filter(|valve| valve.name == "AA" || valve.flow_rate > 0)
        .for_each(|valve| {
            valve_to_flow.insert(valve.name.clone(), valve.flow_rate);
        });
    valve_to_flow
}
