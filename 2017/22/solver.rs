use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::collections::VecDeque;

type Point = (i16, i16);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum State {
    Clean,
    Weakened,
    Flagged,
    Infected,
}

impl State {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Clean),
            '#' => Some(Self::Infected),
            _ => None,
        }
    }

    fn rotations(&self) -> usize {
        match self {
            Self::Weakened => 0,
            Self::Clean => 1,
            Self::Flagged => 2,
            Self::Infected => 3,
        }
    }
}

#[derive(Debug)]
struct Virus {
    grid: FxHashMap<Point, State>,
    state_change: FxHashMap<State, State>,
    position: Point,
    directions: VecDeque<Point>,
    infections: usize,
}

impl Virus {
    fn new(grid: FxHashMap<Point, State>, state_change: FxHashMap<State, State>) -> Self {
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
        let state = self.grid.get(&self.position).unwrap_or(&State::Clean);
        self.directions.rotate_left(state.rotations());
        let (dx, dy) = self.directions.front().unwrap();
        let new_state = self.state_change.get(state).unwrap();
        self.grid.insert(self.position, new_state.clone());
        self.infections += match new_state {
            State::Infected => 1,
            _ => 0,
        };
        self.position = (self.position.0 + dx, self.position.1 + dy);
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let simplified = [
        (State::Clean, State::Infected),
        (State::Infected, State::Clean),
    ];
    answer::part1(5575, run(10_000, simplified.into_iter().collect()));
    let expanded = [
        (State::Clean, State::Weakened),
        (State::Weakened, State::Infected),
        (State::Infected, State::Flagged),
        (State::Flagged, State::Clean),
    ];
    answer::part2(2511991, run(10_000_000, expanded.into_iter().collect()));
}

fn run(n: usize, state_change: FxHashMap<State, State>) -> usize {
    let mut grid: FxHashMap<Point, State> = FxHashMap::default();
    for (y, line) in Reader::default().read_lines().iter().enumerate() {
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
