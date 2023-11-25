use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::{HashMap, VecDeque};

type Point = (i16, i16);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum State {
    CLEAN,
    WEAKENED,
    FLAGGED,
    INFECTED,
}

impl State {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::CLEAN),
            '#' => Some(Self::INFECTED),
            _ => None,
        }
    }

    fn rotations(&self) -> usize {
        match self {
            Self::WEAKENED => 0,
            Self::CLEAN => 1,
            Self::FLAGGED => 2,
            Self::INFECTED => 3,
        }
    }
}

#[derive(Debug)]
struct Virus {
    grid: HashMap<Point, State>,
    state_change: HashMap<State, State>,
    position: Point,
    directions: VecDeque<Point>,
    infections: usize,
}

impl Virus {
    fn new(grid: HashMap<Point, State>, state_change: HashMap<State, State>) -> Self {
        let (mut x, mut y) = (0, 0);
        for point in grid.keys() {
            (x, y) = (x.max(point.0), y.max(point.1));
        }
        Self {
            grid,
            state_change,
            position: (x / 2, y / 2),
            directions: [(0, -1), (-1, 0), (0, 1), (1, 0)].into(),
            infections: 0,
        }
    }

    fn burst(&mut self) {
        let state = self.grid.get(&self.position).unwrap_or(&State::CLEAN);
        self.directions.rotate_left(state.rotations());
        let (dx, dy) = self.directions.front().unwrap();
        let new_state = self.state_change.get(state).unwrap();
        self.grid.insert(self.position.clone(), new_state.clone());
        self.infections += match new_state {
            State::INFECTED => 1,
            _ => 0,
        };
        self.position = (self.position.0 + dx, self.position.1 + dy);
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
    let mut grid: HashMap<Point, State> = HashMap::new();
    for (y, line) in reader::read_lines().iter().enumerate() {
        for (x, ch) in line.char_indices() {
            grid.insert((x as i16, y as i16), State::from_char(ch).unwrap());
        }
    }
    let mut virus = Virus::new(grid, state_change);
    for _ in 0..n {
        virus.burst();
    }
    virus.infections
}
