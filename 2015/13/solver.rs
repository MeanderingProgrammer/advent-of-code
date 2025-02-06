use aoc::{answer, HashMap, HashSet, Iter, Reader};

type Graph<'a> = HashMap<(&'a str, &'a str), i16>;

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
    let mut graph: Graph = HashMap::default();
    let lines = Reader::default().lines::<String>();
    lines.iter().for_each(|line| {
        let mut it = line.split_whitespace();
        let start = it.next().unwrap();
        let effect = it.nth(1).unwrap();
        let weight: i16 = it.next().unwrap().parse().unwrap();
        let multiplier: i16 = match effect {
            "gain" => 1,
            "lose" => -1,
            _ => panic!("Unknown multiplier"),
        };
        let end = it.nth(6).unwrap().trim_matches('.');
        graph.insert((start, end), multiplier * weight);
    });
    answer::part1(709, max_score(&graph, false));
    answer::part2(668, max_score(&graph, true));
}

fn max_score(graph: &Graph, include_self: bool) -> i16 {
    let mut all_people: HashSet<&str> = graph.keys().map(|pair| pair.0).collect();
    if include_self {
        all_people.insert("Myself");
    }
    all_people
        .into_iter()
        .permutations()
        .map(|people| People { people, graph }.score())
        .max()
        .unwrap()
}
