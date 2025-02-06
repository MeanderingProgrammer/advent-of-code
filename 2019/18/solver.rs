use aoc::{
    answer, BitSet, Convert, Dijkstra, FromChar, Grid, HashMap, HashSet, Heading, Ids, Point,
    Reader,
};
use std::collections::VecDeque;

#[derive(Debug, Clone)]
enum Element {
    Start,
    Empty,
    Key(u8),
    Door(u8),
}

impl FromChar for Element {
    fn from_char(ch: char) -> Option<Self> {
        if ch == '#' {
            None
        } else if ch == '@' {
            Some(Self::Start)
        } else if ch == '.' {
            Some(Self::Empty)
        } else if ch.is_ascii_lowercase() {
            Some(Self::Key(Convert::idx_lower(ch)))
        } else if ch.is_ascii_uppercase() {
            Some(Self::Door(Convert::idx_upper(ch)))
        } else {
            None
        }
    }
}

impl Element {
    fn is_start(&self) -> bool {
        matches!(self, Self::Start)
    }

    fn is_key(&self) -> bool {
        matches!(self, Self::Key(_))
    }

    fn is_main(&self) -> bool {
        self.is_start() || self.is_key()
    }
}

#[derive(Debug)]
struct Path {
    point: u8,
    key: u8,
    need: BitSet,
    distance: u16,
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct State {
    points: Vec<u8>,
    keys: BitSet,
}

impl State {
    fn take(&self, path: &Path) -> bool {
        if self.keys.contains(path.key) {
            // Skip keys we already have
            false
        } else {
            // Ensure we have all the keys we need
            path.need.values().all(|key| self.keys.contains(key))
        }
    }
}

#[derive(Debug)]
struct Maze {
    graph: HashMap<u8, Vec<Path>>,
    keys: usize,
}

impl Dijkstra for Maze {
    type T = State;
    type W = u16;

    fn done(&self, node: &Self::T) -> bool {
        node.keys.values().count() == self.keys
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        node.points.iter().enumerate().flat_map(move |(i, point)| {
            self.graph[point]
                .iter()
                .filter(|path| node.take(path))
                .map(move |path| {
                    let mut points = node.points.clone();
                    points[i] = path.point;
                    let keys = node.keys.extend([path.key]);
                    (State { points, keys }, path.distance)
                })
        })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    answer::part1(5402, solve(grid.clone()));
    answer::part2(2138, solve(split(grid.clone())));
}

fn split(mut grid: Grid<Element>) -> Grid<Element> {
    let start = grid
        .iter()
        .find(|(_, value)| value.is_start())
        .map(|(point, _)| point.clone())
        .unwrap();

    grid.remove(&start);
    start
        .neighbors()
        .iter()
        .for_each(|point| grid.remove(point));

    let starts = [
        Heading::NorthEast,
        Heading::NorthWest,
        Heading::SouthEast,
        Heading::SouthWest,
    ];
    starts
        .iter()
        .map(|heading| start.add(heading))
        .for_each(|point| grid.add(point, Element::Start));

    grid
}

fn solve(grid: Grid<Element>) -> u16 {
    let mut ids = Ids::default();
    let mut graph = HashMap::default();
    grid.iter()
        .filter(|(_, value)| value.is_main())
        .for_each(|(point, _)| {
            let paths = get_paths(&grid, point, &mut ids);
            graph.insert(ids.set(point) as u8, paths);
        });

    let keys = grid.iter().filter(|(_, value)| value.is_key()).count();

    let maze = Maze { graph, keys };
    let start = State {
        points: grid
            .iter()
            .filter(|(_, value)| value.is_start())
            .map(|(point, _)| ids.set(point) as u8)
            .collect(),
        keys: BitSet::default(),
    };
    maze.run(start).unwrap()
}

fn get_paths(grid: &Grid<Element>, start: &Point, ids: &mut Ids<Point>) -> Vec<Path> {
    let mut queue = VecDeque::default();
    queue.push_back(((start.clone(), BitSet::default()), 0));
    let mut seen = HashSet::default();
    let mut result = Vec::default();
    while !queue.is_empty() {
        let ((point, need), distance) = queue.pop_front().unwrap();

        if seen.contains(&point) {
            continue;
        }
        seen.insert(point.clone());

        if &point != start {
            if let Element::Key(key) = grid[&point] {
                result.push(Path {
                    point: ids.set(&point) as u8,
                    key,
                    need: need.clone(),
                    distance,
                });
            }
        }

        for adjacent in point.neighbors() {
            if !seen.contains(&adjacent) {
                let next = match grid.get(&adjacent) {
                    Some(Element::Door(key)) => Some(need.extend([*key])),
                    Some(_) => Some(need.clone()),
                    None => None,
                };
                if let Some(next) = next {
                    queue.push_back(((adjacent, next), distance + 1));
                }
            }
        }
    }
    result
}
