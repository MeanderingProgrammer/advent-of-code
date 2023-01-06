use aoc_lib::answer;
use aoc_lib::reader;
use nom::{
    branch::alt,
    bytes::complete::tag,
    character::complete::{alpha0, digit0},
    combinator::map_res,
    error::Error,
    multi::separated_list0,
    sequence::{separated_pair, tuple},
};
use petgraph::{
    algo::floyd_warshall::floyd_warshall,
    graphmap::DiGraphMap,
};
use priority_queue::PriorityQueue;
use std::collections::HashMap;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct IndividualState {
    location: String,
    minutes_left: i64,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct FullState {
    individuals: Vec<IndividualState>,
    valves_opened: Vec<String>,
}

#[derive(Debug)]
struct Cave<'a> {
    graph: DiGraphMap<&'a str, i64>,
    valve_to_flow: &'a HashMap<String, i64>,
}

impl<'a> Cave<'a> {
    fn next_options(&self, state: &FullState, score: i64, i: usize) -> Vec<(FullState, i64)> {
        let individual = &state.individuals[i];
        self.graph.edges(&individual.location)
            .map(|(_, destination, &time)| (destination, time))
            .filter(|(_, time)| individual.minutes_left - time > 0)
            .filter(|(destination, _)| !state.valves_opened.contains(&(destination.to_owned().to_owned())))
            .map(|(destination, time)| {
                let next_time_left = individual.minutes_left - time - 1;
                let flow_rate = self.valve_to_flow.get(destination).unwrap();

                let mut next_valves_opened = state.valves_opened.clone();
                next_valves_opened.push(destination.to_string());
                next_valves_opened.sort();

                let mut next_individuals = state.individuals.clone();
                next_individuals[i] = IndividualState {
                    location: destination.to_string(),
                    minutes_left: next_time_left,
                };

                let next_state = FullState {
                    individuals: next_individuals,
                    valves_opened: next_valves_opened,
                };
                let next_score = score + (flow_rate * next_time_left);

                (next_state, next_score)
            })
            .collect()
    }

    fn optimistic_additional_score(&self, state: &FullState) -> i64 {
        let mut unopened: Vec<i64> = self.valve_to_flow.iter()
            .filter(|(name, _)| !state.valves_opened.contains(name))
            .map(|(_, &flow_rate)| flow_rate)
            .collect();
        unopened.sort();
        unopened.reverse();

        let mut highest_values = unopened.iter().peekable();

        let mut times_left: Vec<i64> = state.individuals.iter()
            .map(|individual| individual.minutes_left)
            .collect();

        let mut additional_score = 0;
        while times_left.iter().max().unwrap() > &2 && !highest_values.peek().is_none() {
            let index_of_max = times_left.iter().enumerate()
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
    flow_rate: i64,
    leads_to: Vec<String>,
}

impl Valve {
    fn new(name: &str, flow_rate: i64, leads_to: Vec<&str>) -> Result<Self, String> {
        Ok(Self {
            name: name.to_string(),
            flow_rate: flow_rate,
            leads_to: leads_to.iter()
                .map(|to| to.to_string())
                .collect(),
        })
    }
}

fn main() {
    let lines = reader::read_lines();
    let valves = parse(lines.as_slice());
    let valve_to_flow = get_valve_to_flow(&valves);
    let cave = create_cave(&valves, &valve_to_flow);

    answer::part1(1873, traverse_cave(&cave, 30, 1).unwrap());
    answer::part2(2425, traverse_cave(&cave, 26, 2).unwrap());
}

fn traverse_cave(cave: &Cave, starting_time: i64, individuals: usize) -> Option<i64> {
    let mut queue = PriorityQueue::new();
    let mut max_score = None;

    let starting_state = FullState {
        individuals: vec![
            IndividualState {
                location: "AA".to_string(),
                minutes_left: starting_time,
            }; individuals
        ],
        valves_opened: vec!["AA".to_string()],
    };

    queue.push(starting_state, 0);

    while !queue.is_empty() {
        let (state, score) = queue.pop().unwrap();

        if max_score == None || max_score.unwrap() < score {
            max_score = Some(score);
        }

        // Mechanism to filter out states that cannot possibly reach an already seen value
        if max_score != None && score + cave.optimistic_additional_score(&state) < max_score.unwrap() {
            continue;
        }

        let mut across_individuals = vec![
            (state, score),
        ];

        for i in 0..individuals {
            let mut next_options = Vec::new();
            for (state, score) in &across_individuals {
                let options = cave.next_options(state, *score, i);
                if options.len() == 0 && i < individuals - 1 {
                    next_options = across_individuals.clone();
                } else {
                    for (next_state, next_score) in options {
                        next_options.push((next_state, next_score));
                    }
                }
            }
            across_individuals = next_options;
        }

        for (next_state, next_score) in across_individuals {
            queue.push_increase(next_state, next_score);
        }
    }

    max_score
}

fn create_cave<'a>(valves: &'a Vec<Valve>, valve_to_flow: &'a HashMap<String, i64>) -> Cave<'a> {
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
    let mut graph: DiGraphMap<&str, i64> = DiGraphMap::new();
    for v1 in valve_to_flow.keys() {
        for v2 in valve_to_flow.keys() {
            if v1 != v2 {
                let weight = all_distances.get(&(v1, v2)).unwrap();
                graph.add_edge(v1, v2, *weight);
            }
        }
    }

    Cave {
        graph,
        valve_to_flow,
    }
}

fn get_valve_to_flow(valves: &Vec<Valve>) -> HashMap<String, i64> {
    let mut valve_to_flow = HashMap::new();
    valves.iter()
        // Only some of the valves actually matter, in particular the ones with some flow rate + start
        .filter(|valve| valve.name.clone() == "AA" || valve.flow_rate > 0)
        .for_each(|valve| {
            valve_to_flow.insert(valve.name.clone(), valve.flow_rate);
        });
    valve_to_flow
}

fn parse(values: &[String]) -> Vec<Valve> {
    let mut parser = map_res::<_, _, _, Error<_>, _, _, _>(
        separated_pair(
            tuple((
                tag("Valve "),
                alpha0,
                tag(" has flow rate="),
                map_res(digit0, |s: &str| s.parse::<i64>()),
            )),
            tag("; "),
            tuple((
                alt((
                    tag("tunnel leads to valve "),
                    tag("tunnels lead to valves "),
                )),
                separated_list0(
                    tag(", "),
                    alpha0,
                ),
            )),
        ),
        |((_, name, _, flow_rate), (_, leads_to))| Valve::new(name, flow_rate, leads_to),
    );

    values.iter()
        .map(|value| parser(value).unwrap().1)
        .collect()
}
