use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};
use priority_queue::DoublePriorityQueue;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    point: Point,
    direction: Direction,
}

impl State {
    fn new(point: Point, direction: Direction) -> Self {
        Self { point, direction }
    }

    fn next(&self) -> Self {
        Self::new(&self.point + &self.direction, self.direction.clone())
    }

    fn turn(&self, left: bool) -> Self {
        let direction = if left {
            self.direction.left()
        } else {
            self.direction.right()
        };
        Self::new(self.point.clone(), direction)
    }
}

#[derive(Debug)]
struct Maze {
    grid: Grid<char>,
    start: Point,
    end: Point,
}

impl Maze {
    fn new(mut grid: Grid<char>) -> Self {
        let start = grid.points_with_value('S')[0].clone();
        let end = grid.points_with_value('E')[0].clone();
        grid.add(start.clone(), '.');
        grid.add(end.clone(), '.');
        Self { grid, start, end }
    }

    fn solve(&self) -> (usize, usize) {
        let start = State::new(self.start.clone(), Direction::Right);
        let mut min_cost = 0;

        let mut distances = FxHashMap::default();
        distances.insert(start.clone(), 0);

        let mut state_paths = FxHashMap::default();
        state_paths.insert(start.clone(), vec![vec![start.point.clone()]]);

        let mut queue = DoublePriorityQueue::new();
        queue.push(start, 0);

        while !queue.is_empty() {
            let (current, current_cost) = queue.pop_min().unwrap();
            if min_cost > 0 && current_cost > min_cost {
                continue;
            }
            if current.point == self.end {
                min_cost = current_cost;
                continue;
            }
            let neighbors = vec![
                (current.next(), 1),
                (current.turn(true).next(), 1001),
                (current.turn(false).next(), 1001),
            ];
            for (next, next_cost) in neighbors.into_iter() {
                if self.grid.get(&next.point) != &'.' {
                    continue;
                }
                let cost = current_cost + next_cost;
                if !distances.contains_key(&next) || cost < distances[&next] {
                    distances.insert(next.clone(), cost);
                    queue.push(next.clone(), cost);
                    let mut paths = vec![];
                    for path in state_paths[&current].iter() {
                        let mut path = path.clone();
                        path.push(next.point.clone());
                        paths.push(path);
                    }
                    state_paths.insert(next, paths);
                } else if cost == distances[&next] {
                    let mut paths = vec![];
                    for path in state_paths[&current].iter() {
                        let mut path = path.clone();
                        path.push(next.point.clone());
                        paths.push(path);
                    }
                    state_paths.get_mut(&next).unwrap().append(&mut paths);
                }
            }
        }

        let mut seen = FxHashSet::default();
        for (state, paths) in state_paths.into_iter() {
            if state.point != self.end {
                continue;
            }
            for path in paths.iter() {
                for point in path.iter() {
                    seen.insert(point.clone());
                }
            }
        }
        (min_cost, seen.len())
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    let maze = Maze::new(grid);
    let (part1, part2) = maze.solve();
    answer::part1(107512, part1);
    answer::part2(561, part2);
}
