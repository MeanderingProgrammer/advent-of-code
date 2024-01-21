use aoc_lib::answer;
use aoc_lib::reader::Reader;
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

type Graph<'a> = HashMap<(&'a str, &'a str), i64>;

#[derive(Debug)]
struct People<'a> {
    people: Vec<&'a str>,
    graph: &'a Graph<'a>,
}

impl<'a> People<'a> {
    fn score(&self) -> i64 {
        self.people
            .iter()
            .enumerate()
            .map(|(i, person)| self.get(person, i - 1) + self.get(person, i + 1))
            .sum()
    }

    fn get(&self, person: &str, i: usize) -> i64 {
        let neighbor = &self.people[(i + self.people.len()) % self.people.len()];
        *self.graph.get(&(person, neighbor)).unwrap_or(&0)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut graph: Graph = HashMap::new();
    let lines = Reader::default().read_lines();
    lines.iter().for_each(|line| {
        let parts: Vec<&str> = line[0..line.len() - 1].split_whitespace().collect();
        let multiplier: i64 = match parts[2] {
            "gain" => 1,
            "lose" => -1,
            _ => panic!("Unknown multiplier"),
        };
        graph.insert(
            (parts[0], parts[10]),
            multiplier * parts[3].parse::<i64>().unwrap(),
        );
    });
    answer::part1(709, max_score(&graph, false));
    answer::part2(668, max_score(&graph, true));
}

fn max_score(graph: &Graph, include_self: bool) -> i64 {
    let mut all_people: HashSet<&str> = graph.keys().map(|pair| pair.0).collect();
    if include_self {
        all_people.insert("Myself");
    }
    let num_people = all_people.len();
    all_people
        .into_iter()
        .permutations(num_people)
        .map(|people| People { people, graph }.score())
        .max()
        .unwrap()
}
