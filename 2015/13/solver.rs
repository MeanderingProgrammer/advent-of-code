use aoc_lib::answer;
use aoc_lib::reader;
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

type Graph = HashMap<(String, String), i64>;

#[derive(Debug)]
struct People {
    people: Vec<String>,
}

impl People {
    fn score(&self, graph: &Graph) -> i64 {
        self.people
            .iter()
            .enumerate()
            .map(|(i, person)| self.get(person, graph, i - 1) + self.get(person, graph, i + 1))
            .sum()
    }

    fn get(&self, person: &str, graph: &Graph, i: usize) -> i64 {
        let neighbor = &self.people[(i + self.people.len()) % self.people.len()];
        *graph
            .get(&(person.to_string(), neighbor.to_string()))
            .unwrap_or(&0)
    }
}

fn main() {
    let graph = get_graph();
    answer::part1(709, max_score(&graph, false));
    answer::part2(668, max_score(&graph, true));
}

fn get_graph() -> Graph {
    let mut graph = HashMap::new();
    reader::read_lines().into_iter().for_each(|line| {
        let parts: Vec<&str> = line[0..line.len() - 1].split_whitespace().collect();
        let multiplier: Option<i64> = match parts[2] {
            "gain" => Some(1),
            "lose" => Some(-1),
            _ => None,
        };
        graph.insert(
            (parts[0].to_string(), parts[10].to_string()),
            multiplier.unwrap() * parts[3].parse::<i64>().unwrap(),
        );
    });
    graph
}

fn max_score(graph: &Graph, include_self: bool) -> i64 {
    let mut all_people: HashSet<String> = graph.keys().map(|pair| pair.0.clone()).collect();
    if include_self {
        all_people.insert("Myself".to_string());
    }
    let num_people = all_people.len();
    all_people
        .into_iter()
        .permutations(num_people)
        .map(|people| People { people }.score(graph))
        .max()
        .unwrap()
}
