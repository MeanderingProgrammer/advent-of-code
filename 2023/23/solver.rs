use aoc::{answer, BitSet, Direction, FromChar, Grid, HashMap, Ids, Point, Reader};
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
        let start = bounds.lower.add(&Direction::Right);
        let target = bounds.upper.add(&Direction::Left);

        // Save space and make lookups faster by mapping points to an integer
        let mut ids: Ids<Point> = Ids::default();
        let mut graph: HashMap<Point, HashMap<Direction, Edge>> = HashMap::default();

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
                ids.set(start);
                // Add current edge to the graph
                graph.entry(start.clone()).or_default().insert(
                    trace.dir,
                    Edge {
                        id: ids.set(end) as u8,
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
                (ids.get(&point) as u8, edges)
            })
            .collect();

        Search {
            start: ids.get(&start) as u8,
            target: ids.get(&target) as u8,
            graph,
        }
    }

    fn neighbors(&self, trace: &Trace) -> Vec<(Point, Direction, bool)> {
        let last = trace.path.last().unwrap();
        let value = self.grid[last];
        Direction::values()
            .iter()
            // Continue path in all directions from last point on our path
            .map(|dir| (last.add(dir), dir.clone()))
            // Remove anything that's off the grid or goes into a forest
            .filter(|(point, _)| self.grid.get_or(point, '#') != '#')
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
}

#[derive(Debug)]
struct State {
    seen: BitSet,
    last: u8,
    length: usize,
}

impl State {
    fn new(start: u8) -> Self {
        Self {
            seen: [start].into(),
            last: start,
            length: 0,
        }
    }

    fn add(&self, edge: &Edge) -> Self {
        Self {
            seen: self.seen.extend([edge.id]),
            last: edge.id,
            length: self.length + edge.length,
        }
    }
}

#[derive(Debug)]
struct Search {
    start: u8,
    target: u8,
    graph: HashMap<u8, Vec<Edge>>,
}

impl Search {
    fn run(&self, slippery: bool) -> usize {
        let mut result: usize = 0;
        let mut q: VecDeque<State> = VecDeque::default();
        q.push_back(State::new(self.start));
        while let Some(state) = q.pop_back() {
            if state.last == self.target {
                result = result.max(state.length);
            } else {
                self.graph[&state.last]
                    .iter()
                    .filter(|edge| !slippery || !edge.uphill)
                    .filter(|edge| !state.seen.contains(edge.id))
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
    let grid = Reader::default().read_grid();
    let search = Compress { grid }.collapse();
    answer::part1(2154, search.run(true));
    answer::part2(6654, search.run(false));
}
