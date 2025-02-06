use aoc::{answer, Direction, Grid, HashSet, Iter, Point, Reader};
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    point: Point,
    direction: Direction,
}

impl State {
    fn new(point: Point, direction: Direction) -> Self {
        Self { point, direction }
    }

    fn next_states<'a>(&'a self, grid: &'a Grid<char>) -> impl Iterator<Item = State> + 'a {
        self.next_directions(grid)
            .map(|direction| Self::new(self.point.add(&direction), direction))
            .filter(|state| grid.has(&state.point))
    }

    fn next_directions(&self, grid: &Grid<char>) -> impl Iterator<Item = Direction> {
        match grid[&self.point] {
            '.' => vec![self.direction.clone()],
            '|' => match self.direction {
                Direction::Up | Direction::Down => vec![self.direction.clone()],
                Direction::Left | Direction::Right => vec![Direction::Up, Direction::Down],
            },
            '-' => match self.direction {
                Direction::Up | Direction::Down => vec![Direction::Left, Direction::Right],
                Direction::Left | Direction::Right => vec![self.direction.clone()],
            },
            '\\' => match self.direction {
                Direction::Up => vec![Direction::Left],
                Direction::Down => vec![Direction::Right],
                Direction::Left => vec![Direction::Up],
                Direction::Right => vec![Direction::Down],
            },
            '/' => match self.direction {
                Direction::Up => vec![Direction::Right],
                Direction::Down => vec![Direction::Left],
                Direction::Left => vec![Direction::Down],
                Direction::Right => vec![Direction::Up],
            },
            value => panic!("Invalid argument: {}", value),
        }
        .into_iter()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    answer::part1(8901, part1(&grid));
    answer::part2(9064, part2(&grid));
}

fn part1(grid: &Grid<char>) -> usize {
    energized(grid, State::new(Point::default(), Direction::Right))
}

fn part2(grid: &Grid<char>) -> usize {
    let bounds = grid.bounds();
    let (start, end) = (bounds.lower.x, bounds.upper.x);
    let coords: Vec<i32> = (start..=end).collect();
    states(&coords, Direction::Down, |x| Point::new(x, start))
        .chain(states(&coords, Direction::Up, |x| Point::new(x, end)))
        .chain(states(&coords, Direction::Right, |y| Point::new(start, y)))
        .chain(states(&coords, Direction::Left, |y| Point::new(end, y)))
        .map(|state| energized(grid, state))
        .max()
        .unwrap()
}

fn states<'a, F: Fn(i32) -> Point + 'a>(
    coords: &'a [i32],
    direction: Direction,
    f: F,
) -> impl Iterator<Item = State> + 'a {
    coords
        .iter()
        .map(move |&coord| State::new(f(coord), direction.clone()))
}

fn energized(grid: &Grid<char>, start: State) -> usize {
    let mut explored = HashSet::default();
    explored.insert(start.clone());
    let mut q: VecDeque<State> = VecDeque::default();
    q.push_back(start);
    while let Some(state) = q.pop_front() {
        state.next_states(grid).for_each(|state| {
            if explored.insert(state.clone()) {
                q.push_back(state);
            }
        });
    }
    explored.into_iter().map(|state| state.point).unique()
}
