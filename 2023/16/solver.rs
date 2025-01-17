use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    position: Point,
    direction: Direction,
}

impl State {
    fn new(position: Point, direction: Direction) -> Self {
        Self {
            position,
            direction,
        }
    }

    fn next_states<'a>(&'a self, grid: &'a Grid<char>) -> impl Iterator<Item = State> + 'a {
        self.next_directions(grid)
            .map(|direction| Self::new(self.position.add(&direction), direction))
            .filter(|state| grid.contains(&state.position))
    }

    fn next_directions(&self, grid: &Grid<char>) -> impl Iterator<Item = Direction> {
        match *grid.get(&self.position) {
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

fn energized(grid: &Grid<char>, start: State) -> usize {
    let mut explored = FxHashSet::default();
    explored.insert(start.clone());
    let mut q: VecDeque<State> = VecDeque::default();
    q.push_back(start);
    while !q.is_empty() {
        let state = q.pop_front().unwrap();
        state.next_states(grid).for_each(|state| {
            if explored.insert(state.clone()) {
                q.push_back(state);
            }
        });
    }
    explored
        .into_iter()
        .map(|state| state.position)
        .collect::<FxHashSet<_>>()
        .len()
}

fn create_states<'a, F: Fn(i64) -> Point + 'a>(
    coords: &'a [i64],
    direction: Direction,
    f: F,
) -> impl Iterator<Item = State> + 'a {
    coords
        .iter()
        .map(move |&coord| State::new(f(coord), direction.clone()))
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);

    let part1 = energized(&grid, State::new(Point::default(), Direction::Right));

    let side = grid.bounds().upper.x;
    let coords: Vec<i64> = (0..=side).collect();
    let part2 = create_states(&coords, Direction::Down, |x| Point::new(x, 0))
        .chain(create_states(&coords, Direction::Up, |x| {
            Point::new(x, side)
        }))
        .chain(create_states(&coords, Direction::Right, |y| {
            Point::new(0, y)
        }))
        .chain(create_states(&coords, Direction::Left, |y| {
            Point::new(side, y)
        }))
        .map(|state| energized(&grid, state))
        .max()
        .unwrap();

    answer::part1(8901, part1);
    answer::part2(9064, part2);
}
