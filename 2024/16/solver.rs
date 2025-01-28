use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::queue::{HeapVariant, PriorityQueue};
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};

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
        Self::new(self.point.add(&self.direction), self.direction.clone())
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
        let (start, end) = (grid.value(&'S'), grid.value(&'E'));
        grid.add(start.clone(), '.');
        grid.add(end.clone(), '.');
        Self { grid, start, end }
    }

    fn solve(&self) -> (usize, usize) {
        let mut min_cost = 0;
        let mut end_seen = FxHashSet::default();

        let start = State::new(self.start.clone(), Direction::Right);

        let mut distances = FxHashMap::default();
        distances.insert(start.clone(), 0);

        let mut start_seen = FxHashSet::default();
        start_seen.insert(start.point.clone());
        let mut state_seen = FxHashMap::default();
        state_seen.insert(start.clone(), start_seen);

        let mut queue = PriorityQueue::new(HeapVariant::Min);
        queue.push(start, 0);

        while !queue.is_empty() {
            let (current, current_cost) = queue.pop().unwrap();
            if min_cost > 0 && current_cost > min_cost {
                continue;
            }
            if current.point == self.end {
                min_cost = current_cost;
                end_seen.extend(state_seen[&current].clone());
                continue;
            }
            let neighbors = vec![
                (current.next(), 1),
                (current.turn(true).next(), 1001),
                (current.turn(false).next(), 1001),
            ];
            for (next, next_cost) in neighbors.into_iter() {
                if self.grid[&next.point] != '.' {
                    continue;
                }
                let cost = current_cost + next_cost;
                if !distances.contains_key(&next) || cost < distances[&next] {
                    distances.insert(next.clone(), cost);
                    queue.push(next.clone(), cost);
                    let mut seen = state_seen[&current].clone();
                    seen.insert(next.point.clone());
                    state_seen.insert(next, seen);
                } else if cost == distances[&next] {
                    let mut seen = state_seen[&current].clone();
                    seen.insert(next.point.clone());
                    state_seen.get_mut(&next).unwrap().extend(seen);
                }
            }
        }

        (min_cost, end_seen.len())
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
