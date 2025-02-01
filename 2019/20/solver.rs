use aoc::{answer, Dijkstra, Direction, Grid, HashMap, HashSet, Point, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
struct Maze {
    grid: Grid<char>,
    width: usize,
    height: usize,
    size: usize,
}

impl Maze {
    //          A
    //          A
    //   #######.#########
    //   #######.........#
    //   #######.#######.#
    //   #######.#######.#
    //   #######.#######.#
    //   #####  B    ###.#
    // BC...##  C    ###.#
    //   ##.##       ###.#
    //   ##...DE  F  ###.#
    //   #####    G  ###.#
    //   #########.#####.#
    // DE..#######...###.#
    //   #.#########.###.#
    // FG..#########.....#
    //   ###########.#####
    //              Z
    //              Z
    fn new(lines: &[String]) -> Self {
        let middle = &lines[lines.len() / 2];
        Self {
            grid: Grid::from_lines(lines, |_, ch| Some(ch)),
            width: middle.len(),
            height: lines.len(),
            size: middle.chars().filter(|ch| ['#', '.'].contains(ch)).count() / 2,
        }
    }

    fn graph(&self) -> HashMap<Node, Vec<(Node, u16)>> {
        let mut nodes = self.nodes(true);
        nodes.extend(self.nodes(false));
        let mut result = HashMap::default();
        for (point, node) in nodes.iter() {
            result.insert(node.clone(), self.edges(point, &nodes));
        }
        result
    }

    fn nodes(&self, horizontal: bool) -> HashMap<Point, Node> {
        let mut result = HashMap::default();
        let size = if horizontal { self.width } else { self.height };
        let direction = if horizontal {
            Direction::Right
        } else {
            Direction::Down
        };
        let values = [
            (0, true, false),
            (self.size + 2, false, true),
            (size - self.size - 4, true, true),
            (size - 2, false, false),
        ];
        for v1 in 0..size {
            for (v2, after, inner) in values {
                let start = if horizontal {
                    Point::new(v2 as i32, v1 as i32)
                } else {
                    Point::new(v1 as i32, v2 as i32)
                };
                if let Some((point, label)) = self.node(start, &direction, after) {
                    result.insert(point, Node::new(&label, inner));
                }
            }
        }
        result
    }

    fn node(&self, start: Point, direction: &Direction, after: bool) -> Option<(Point, String)> {
        let end = start.add(direction);
        let point = if after {
            end.add(direction)
        } else {
            start.add(&direction.opposite())
        };
        let c1 = self.grid.get_or(&start, ' ');
        let c2 = self.grid.get_or(&end, ' ');
        if c1.is_alphabetic() && c2.is_alphabetic() {
            assert_eq!('.', self.grid[&point]);
            Some((point, format!("{c1}{c2}")))
        } else {
            None
        }
    }

    fn edges(&self, start: &Point, nodes: &HashMap<Point, Node>) -> Vec<(Node, u16)> {
        let mut queue = VecDeque::default();
        queue.push_back((start.clone(), 0));
        let mut seen = HashSet::default();
        let mut result = Vec::default();
        while !queue.is_empty() {
            let (point, length) = queue.pop_front().unwrap();
            if seen.contains(&point) {
                continue;
            }
            seen.insert(point.clone());
            if &point != start && nodes.contains_key(&point) {
                let node = nodes.get(&point).unwrap().clone();
                result.push((node, length));
            } else {
                for adjacent in point.neighbors() {
                    let value = self.grid.get_or(&adjacent, ' ');
                    if value == '.' && !seen.contains(&adjacent) {
                        queue.push_back((adjacent, length + 1));
                    }
                }
            }
        }
        result
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Node {
    label: String,
    inner: bool,
}

impl Node {
    fn new(label: &str, inner: bool) -> Self {
        Self {
            label: label.to_string(),
            inner,
        }
    }

    fn opposite(&self) -> Self {
        Self {
            label: self.label.clone(),
            inner: !self.inner,
        }
    }

    fn end(&self) -> bool {
        ["AA", "ZZ"].contains(&self.label.as_str())
    }
}

#[derive(Debug)]
struct Graph {
    graph: HashMap<Node, Vec<(Node, u16)>>,
    recursive: bool,
}

impl Dijkstra for Graph {
    type T = (Node, u8);
    type W = u16;

    fn done(&self, (node, _): &Self::T) -> bool {
        node == &Node::new("ZZ", false)
    }

    fn neighbors(&self, (node, level): &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        self.graph[node].iter().filter_map(move |(node, length)| {
            let next = if node.end() {
                if *level == 0 {
                    Some((node.clone(), *level, *length))
                } else {
                    None
                }
            } else if !self.recursive {
                Some((node.opposite(), *level, length + 1))
            } else {
                let level = if node.inner {
                    Some(level + 1)
                } else if *level > 0 {
                    Some(level - 1)
                } else {
                    None
                };
                level.map(|level| (node.opposite(), level, length + 1))
            };
            next.map(|(node, level, length)| ((node, level), length))
        })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let graph = Maze::new(&lines).graph();
    answer::part1(628, solve(&graph, false));
    answer::part2(7506, solve(&graph, true));
}

fn solve(graph: &HashMap<Node, Vec<(Node, u16)>>, recursive: bool) -> u16 {
    let graph = graph.clone();
    let start = (Node::new("AA", false), 0);
    Graph { graph, recursive }.run(start).unwrap()
}
