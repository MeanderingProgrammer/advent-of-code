use aoc::{answer, Convert, GraphSearch, HashMap, Parser, Reader};
use std::str::FromStr;

const START: u32 = 0;
const END: u32 = 1;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Cave {
    big: bool,
    value: u32,
}

impl FromStr for Cave {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            big: Convert::ch(s).is_uppercase(),
            value: if s == "start" {
                START
            } else if s == "end" {
                END
            } else {
                Convert::idx_lower_str(s)
            },
        })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Path {
    caves: Vec<Cave>,
    duplicate: bool,
}

impl Path {
    fn new(cave: Cave) -> Self {
        Self {
            caves: vec![cave],
            duplicate: false,
        }
    }

    fn add(&self, cave: Cave) -> Self {
        let mut next = self.clone();
        if !next.duplicate && !cave.big && next.caves.contains(&cave) {
            next.duplicate = true;
        }
        next.caves.push(cave);
        next
    }
}

#[derive(Debug)]
struct Search {
    graph: HashMap<Cave, Vec<Cave>>,
    valid: fn(&Path, &Cave) -> bool,
}

impl GraphSearch for Search {
    type T = Path;

    fn first(&self) -> bool {
        false
    }

    fn done(&self, node: &Self::T) -> bool {
        node.caves.last().unwrap().value == END
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = Self::T> {
        self.graph
            .get(node.caves.last().unwrap())
            .unwrap()
            .iter()
            .filter(|cave| (self.valid)(node, cave))
            .map(|cave| node.add(cave.clone()))
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let graph = get_graph(&lines);
    answer::part1(3497, paths(graph.clone(), true));
    answer::part2(93686, paths(graph.clone(), false));
}

fn get_graph(lines: &[String]) -> HashMap<Cave, Vec<Cave>> {
    let mut graph: HashMap<Cave, Vec<Cave>> = HashMap::default();
    lines.iter().for_each(|line| {
        let [c1, c2]: [Cave; 2] = Parser::values(line, "-").unwrap();
        graph.entry(c1.clone()).or_default().push(c2.clone());
        graph.entry(c2.clone()).or_default().push(c1.clone());
    });
    graph
}

fn paths(graph: HashMap<Cave, Vec<Cave>>, part1: bool) -> usize {
    let valid = if part1 { one_small } else { two_small };
    let search = Search { graph, valid };
    search.dfs(Path::new("start".parse().unwrap())).len()
}

fn one_small(path: &Path, cave: &Cave) -> bool {
    if cave.big {
        true
    } else {
        !path.caves.contains(cave)
    }
}

fn two_small(path: &Path, cave: &Cave) -> bool {
    if cave.big {
        true
    } else if cave.value == START {
        false
    } else if !path.duplicate {
        true
    } else {
        !path.caves.contains(cave)
    }
}
