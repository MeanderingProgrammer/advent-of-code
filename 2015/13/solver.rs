use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};
use itertools::Itertools;

type Graph<'a> = FxHashMap<(&'a str, &'a str), i16>;

#[derive(Debug)]
struct People<'a> {
    people: Vec<&'a str>,
    graph: &'a Graph<'a>,
}

impl People<'_> {
    fn score(&self) -> i16 {
        self.people
            .iter()
            .enumerate()
            .map(|(i, person)| (i as i16, person))
            .map(|(i, person)| self.get(i - 1, person) + self.get(i + 1, person))
            .sum()
    }

    fn get(&self, i: i16, person: &str) -> i16 {
        let neighbor = &self.people[i.rem_euclid(self.people.len() as i16) as usize];
        *self.graph.get(&(person, neighbor)).unwrap_or(&0)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut graph: Graph = FxHashMap::default();
    let lines = Reader::default().read_lines();
    lines.iter().for_each(|line| {
        let parts: Vec<&str> = line[0..line.len() - 1].split_whitespace().collect();
        let multiplier: i16 = match parts[2] {
            "gain" => 1,
            "lose" => -1,
            _ => panic!("Unknown multiplier"),
        };
        graph.insert(
            (parts[0], parts[10]),
            multiplier * parts[3].parse::<i16>().unwrap(),
        );
    });
    answer::part1(709, max_score(&graph, false));
    answer::part2(668, max_score(&graph, true));
}

fn max_score(graph: &Graph, include_self: bool) -> i16 {
    let mut all_people: FxHashSet<&str> = graph.keys().map(|pair| pair.0).collect();
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
