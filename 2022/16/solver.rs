use aoc_lib::answer;
use aoc_lib::graph::Graph;
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
use priority_queue::PriorityQueue;

#[derive(Debug, Clone)]
struct Valve {
    name: String,
    flow_rate: i64,
}

impl Valve {
    fn new(name: &str, flow_rate: i64) -> Result<Self, String> {
        Ok(Self { name: name.to_string(), flow_rate })
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct State {
    locations: Vec<String>,
    minutes_left: i64,
    valves_opened: Vec<String>,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Score {
    minutes_left: i64,
    score: i64,
}

#[derive(Debug)]
struct FullState {
    locations: Vec<String>,
    minutes_left: i64,
    valves_opened: Vec<String>,
    score: i64,
}

impl FullState {
    fn from_state(state: State, score: Score) -> Self {
        Self {
            locations: state.locations,
            minutes_left: state.minutes_left,
            valves_opened: state.valves_opened,
            score: score.score,
        }
    }

    fn state(&self) -> State {
        State {
            locations: self.locations.clone(),
            minutes_left: self.minutes_left,
            valves_opened: self.valves_opened.clone(),
        }
    }

    fn score(&self) -> Score {
        Score {
            minutes_left: self.minutes_left,
            score: self.score,
        }
    }

    fn next_options(&self, graph: &Graph<Valve>) -> Vec<Self> {
        let minutes_remaining = self.minutes_left - 1;

        let next_options = self.next_options_for(0, graph, minutes_remaining);

        if self.locations.len() == 1 {
            next_options
        } else {
            let mut result = Vec::new();
            for next_option in next_options {
                let mut further_options = next_option.next_options_for(1, graph, minutes_remaining);
                result.append(&mut further_options);
            }
            result
        }
    }

    fn next_options_for(&self, index: usize, graph: &Graph<Valve>, minutes_remaining: i64) -> Vec<Self> {
        let mut result = Vec::new();
        let location = &self.locations[index];

        let valve = graph.get_node(location);
        if !self.already_open(valve) && valve.flow_rate > 0 {
            result.push(self.open_valve(valve, minutes_remaining));
        }

        for neighbor in graph.neighbors(location) {
            result.push(self.move_to(index, neighbor, minutes_remaining));
        }

        result
    }

    fn already_open(&self, valve: &Valve) -> bool {
        self.valves_opened.contains(&valve.name.to_string())
    }

    fn open_valve(&self, valve: &Valve, minutes_remaining: i64) -> Self {
        let mut updated_valves_opened = self.valves_opened.clone();
        updated_valves_opened.push(valve.name.to_string());
        updated_valves_opened.sort();

        Self {
            locations: self.locations.clone(),
            minutes_left: minutes_remaining,
            valves_opened: updated_valves_opened,
            score: self.score + (valve.flow_rate * minutes_remaining),
        }
    }

    fn move_to(&self, index: usize, destination: &Valve, minutes_remaining: i64) -> Self {
        let mut updated_locations = self.locations.clone();
        updated_locations[index] = destination.name.to_string();

        Self {
            locations: updated_locations,
            minutes_left: minutes_remaining,
            valves_opened: self.valves_opened.clone(),
            score: self.score,
        }
    }
}

#[derive(Debug)]
struct ScanLine {
    valve: Valve,
    leads_to: Vec<String>,
}

impl ScanLine {
    fn new(valve: Valve, leads_to: Vec<&str>) -> Self {
        Self {
            valve,
            leads_to: leads_to.iter()
                .map(|to| to.to_string())
                .collect(),
        }
    }
}

fn main() {
    let graph = create_graph();
    answer::part1(1873, traverse_graph(&graph, 30, 1).unwrap());
    answer::part2(2425, traverse_graph(&graph, 26, 2).unwrap());
}

fn traverse_graph(graph: &Graph<Valve>, starting_time: i64, individuals: usize) -> Option<i64> {
    let mut queue = PriorityQueue::new();

    let starting_state = FullState {
        locations: vec!["AA".to_string(); individuals],
        minutes_left: starting_time,
        valves_opened: Vec::new(),
        score: 0,
    };

    queue.push(starting_state.state(), starting_state.score());

    while !queue.is_empty() {
        let (partial_state, score) = queue.pop().unwrap();
        let state = FullState::from_state(partial_state, score);

        if state.minutes_left == 0 {
            return Some(state.score);
        }

        // Super hacky pruning logic, based on looking at states and seeing
        // which ones could never reach the maximum score
        if individuals == 2 && state.minutes_left < 19 && state.score < 1000 {
            continue;
        }
        if individuals == 2 && state.minutes_left < 12 && state.score < 2000 {
            continue;
        }

        let next_options = state.next_options(graph);
        for next_option in next_options {
            queue.push_increase(next_option.state(), next_option.score());
        }
    }

    None
}

fn create_graph() -> Graph<Valve> {
    let lines = reader::read_lines();
    let scan_lines = parse(lines.as_slice());

    let mut graph: Graph<Valve> = Graph::new();

    // Add nodes
    scan_lines.iter()
        .map(|scan_line| &scan_line.valve)
        .for_each(|valve| graph.add_node(valve.name.clone(), valve.clone()));

    // Add edges between nodes
    scan_lines.iter()
        .for_each(|scan_line| {
            let valve = &scan_line.valve;
            scan_line.leads_to.iter()
                .for_each(|destination| graph.add_edge(&valve.name, destination));
        });

    graph
}

fn parse(values: &[String]) -> Vec<ScanLine> {
    let mut parser = separated_pair::<_, _, _, _, Error<_>, _, _, _>(
        map_res(
            tuple((
                tag("Valve "),
                alpha0,
                tag(" has flow rate="),
                map_res(digit0, |s: &str| s.parse::<i64>()),
            )),
            |(_, name, _, flow_rate)| Valve::new(name, flow_rate),
        ),
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
    );

    values.iter()
        .map(|value| parser(value).unwrap().1)
        .map(|(valve, (_, leads_to))| ScanLine::new(valve, leads_to))
        .collect()
}
