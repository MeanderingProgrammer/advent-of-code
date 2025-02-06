use aoc::{answer, math, HashMap, Parser, Reader};
use std::str::FromStr;

#[derive(Debug)]
struct Edge {
    left: String,
    right: String,
}

impl FromStr for Edge {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // (BBB, CCC)
        let s = Parser::enclosed(s, '(', ')').unwrap();
        let [left, right] = Parser::values(s, ", ").unwrap();
        Ok(Self { left, right })
    }
}

#[derive(Debug)]
struct Network {
    directions: Vec<char>,
    graph: HashMap<String, Edge>,
}

impl Network {
    fn new(groups: &[Vec<String>]) -> Self {
        Self {
            directions: groups[0][0].chars().collect(),
            graph: groups[1]
                .iter()
                .map(|line| {
                    // AAA =  <edge>
                    let (node, edge) = line.split_once(" = ").unwrap();
                    (node.to_string(), edge.parse().unwrap())
                })
                .collect(),
        }
    }

    fn until(&self, start: &str, end: fn(&str) -> bool) -> usize {
        let (mut current, mut i) = (start.to_string(), 0);
        while !end(&current) {
            current = self.step(&current);
            i += 1;
        }
        i * self.directions.len()
    }

    fn step(&self, start: &str) -> String {
        let mut current = start;
        for direction in self.directions.iter() {
            let edge = self.graph.get(current).unwrap();
            current = match direction {
                'L' => &edge.left,
                'R' => &edge.right,
                _ => unreachable!(),
            };
        }
        current.to_string()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().groups();
    let network = Network::new(&groups);
    answer::part1(24253, part1(&network));
    answer::part2(12357789728873, part2(&network));
}

fn part1(network: &Network) -> usize {
    network.until("AAA", |node| node == "ZZZ")
}

fn part2(network: &Network) -> usize {
    let loops: Vec<usize> = network
        .graph
        .keys()
        .filter(|node| node.ends_with('A'))
        .map(|start| network.until(start, |node| node.ends_with('Z')))
        .collect();
    math::lcm(loops)
}
