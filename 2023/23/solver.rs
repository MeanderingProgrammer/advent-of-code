use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};
use std::collections::VecDeque;

#[derive(Debug, PartialEq)]
struct Trace {
    path: Vec<Point>,
    dir: Direction,
    uphill: bool,
}

impl Trace {
    fn add(&mut self, point: Point, uphill: bool) {
        self.path.push(point);
        self.uphill |= uphill;
    }
}

#[derive(Debug)]
struct Edge {
    id: u8,
    length: usize,
    uphill: bool,
}

#[derive(Debug)]
struct Compress {
    grid: Grid<char>,
}

impl Compress {
    // Lots of this grid is single option moves, this method collapses all
    // of this information into a dense representation
    fn collapse(&self) -> Search {
        let bounds = self.grid.bounds();
        let start = &bounds.lower + &Direction::Right;
        let target = &bounds.upper + &Direction::Left;

        // Save space and make lookups faster by mapping points to an integer
        let mut ids: FxHashMap<Point, u8> = FxHashMap::default();
        let mut graph: FxHashMap<Point, FxHashMap<Direction, Edge>> = FxHashMap::default();

        let mut traces: VecDeque<Trace> = VecDeque::default();
        traces.push_back(Trace {
            path: vec![start.clone()],
            dir: Direction::Down,
            uphill: false,
        });
        while !traces.is_empty() {
            let trace = traces.front_mut().unwrap();
            let mut options = self.neighbors(trace);
            if options.len() == 1 {
                let (point, _, uphill) = options.pop().unwrap();
                trace.add(point, uphill);
            } else {
                let trace = traces.pop_front().unwrap();
                let (start, end) = (trace.path.first().unwrap(), trace.path.last().unwrap());
                Self::add_id(&mut ids, start);
                // Add current edge to the graph
                graph.entry(start.clone()).or_default().insert(
                    trace.dir,
                    Edge {
                        id: Self::add_id(&mut ids, end),
                        length: trace.path.len() - 1,
                        uphill: trace.uphill,
                    },
                );
                let additional: Vec<Trace> = options
                    .into_iter()
                    // Check existing edges from the destination to avoid re-exploring options
                    .filter(|(_, dir, _)| match graph.get(end) {
                        None => true,
                        Some(explored) => !explored.contains_key(dir),
                    })
                    .map(|(point, dir, uphill)| Trace {
                        path: vec![end.clone(), point],
                        dir,
                        uphill,
                    })
                    .filter(|trace| !traces.contains(trace))
                    .collect();
                additional.into_iter().for_each(|trace| {
                    traces.push_back(trace);
                });
            }
        }

        // Add the insight about not going up along edges, good description:
        // https://www.reddit.com/r/adventofcode/comments/18oy4pc/comment/kfyvp2g
        let graph = graph
            .into_iter()
            .map(|(point, edges)| {
                let n = edges.len();
                let edges = edges
                    .into_iter()
                    .filter(|(dir, _)| n != 3 || dir != &Direction::Up)
                    .map(|(_, edge)| edge)
                    .collect();
                (*ids.get(&point).unwrap(), edges)
            })
            .collect();

        Search {
            start: *ids.get(&start).unwrap(),
            target: *ids.get(&target).unwrap(),
            graph,
        }
    }

    fn neighbors(&self, trace: &Trace) -> Vec<(Point, Direction, bool)> {
        let last = trace.path.last().unwrap();
        let value = *self.grid.get(last);
        Direction::values()
            .iter()
            // Continue path in all directions from last point on our path
            .map(|dir| (last + dir, dir.clone()))
            // Remove anything that's off the grid or goes into a forest
            .filter(|(point, _)| *self.grid.get_or(point).unwrap_or(&'#') != '#')
            // Remove direction going back the way we traveled
            .filter(|(point, _)| !trace.path.contains(point))
            // Add information about whether the step went uphill
            .map(|(point, dir)| {
                let uphill = match Direction::from_char(value) {
                    None => false,
                    Some(hill) => dir != hill,
                };
                (point, dir, uphill)
            })
            .collect()
    }

    fn add_id(ids: &mut FxHashMap<Point, u8>, point: &Point) -> u8 {
        let id = ids.len() as u8;
        *ids.entry(point.clone()).or_insert(id)
    }
}

#[derive(Debug)]
struct State {
    seen: FxHashSet<u8>,
    last: u8,
    length: usize,
}

impl State {
    fn new(start: u8) -> Self {
        let mut seen = FxHashSet::default();
        seen.insert(start);
        Self {
            seen,
            last: start,
            length: 0,
        }
    }

    fn add(&self, edge: &Edge) -> Self {
        let mut seen = self.seen.clone();
        seen.insert(edge.id);
        Self {
            seen,
            last: edge.id,
            length: self.length + edge.length,
        }
    }
}

#[derive(Debug)]
struct Search {
    start: u8,
    target: u8,
    graph: FxHashMap<u8, Vec<Edge>>,
}

impl Search {
    fn run(&self, slippery: bool) -> usize {
        let mut result: usize = 0;
        let mut q: VecDeque<State> = VecDeque::default();
        q.push_back(State::new(self.start));
        while !q.is_empty() {
            let state = q.pop_back().unwrap();
            if state.last == self.target {
                result = result.max(state.length);
            } else {
                self.graph[&state.last]
                    .iter()
                    .filter(|edge| !slippery || !edge.uphill)
                    .filter(|edge| !state.seen.contains(&edge.id))
                    .for_each(|edge| q.push_back(state.add(edge)));
            }
        }
        result
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    let search = Compress { grid }.collapse();
    answer::part1(2154, search.run(true));
    answer::part2(6654, search.run(false));
}
