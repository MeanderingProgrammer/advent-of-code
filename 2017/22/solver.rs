use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum State {
    CLEAN,
    WEAKENED,
    FLAGGED,
    INFECTED,
}

impl std::fmt::Display for State {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

impl State {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::CLEAN),
            '#' => Some(Self::INFECTED),
            _ => None,
        }
    }

    fn rotate(&self, directions: &mut VecDeque<(i64, i64)>) -> (i64, i64) {
        match self {
            Self::CLEAN => directions.rotate_left(1),
            Self::WEAKENED => (),
            Self::FLAGGED => directions.rotate_left(2),
            Self::INFECTED => directions.rotate_right(1),
        };
        *directions.front().unwrap()
    }
}

#[derive(Debug)]
struct Virus {
    grid: Grid<State>,
    state_change: HashMap<State, State>,
    position: Point,
    directions: VecDeque<(i64, i64)>,
    infections: usize,
}

impl Virus {
    fn new(grid: Grid<State>, state_change: HashMap<State, State>) -> Self {
        let bounds = grid.bounds(0);
        let upper = bounds.upper();
        Self {
            grid,
            state_change,
            position: Point::new_2d(upper.x() / 2, upper.y() / 2),
            directions: [(0, -1), (-1, 0), (0, 1), (1, 0)].into(),
            infections: 0,
        }
    }

    fn burst(&mut self) {
        let state = if self.grid.contains(&self.position) {
            self.grid.get(&self.position).clone()
        } else {
            State::CLEAN
        };

        let new_state = self.state_change.get(&state).unwrap();
        self.grid.add(self.position.clone(), new_state.clone());
        if new_state == &State::INFECTED {
            self.infections += 1;
        }

        let (dx, dy) = state.rotate(&mut self.directions);
        self.position = Point::new_2d(self.position.x() + dx, self.position.y() + dy);
    }
}

fn main() {
    let simplified = HashMap::from([
        (State::CLEAN, State::INFECTED),
        (State::INFECTED, State::CLEAN),
    ]);
    answer::part1(5575, run(10_000, simplified));
    let expanded = HashMap::from([
        (State::CLEAN, State::WEAKENED),
        (State::WEAKENED, State::INFECTED),
        (State::INFECTED, State::FLAGGED),
        (State::FLAGGED, State::CLEAN),
    ]);
    answer::part2(2511991, run(10_000_000, expanded));
}

fn run(n: usize, state_change: HashMap<State, State>) -> usize {
    let grid = reader::read_grid(|ch| State::from_char(ch));
    let mut virus = Virus::new(grid, state_change);
    for _ in 0..n {
        virus.burst();
    }
    virus.infections
}
