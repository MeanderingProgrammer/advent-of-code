use aoc::{answer, FromChar, HashMap, Reader};

type Point = (i16, i16);

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum State {
    Clean,
    Weakened,
    Flagged,
    Infected,
}

impl FromChar for State {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Clean),
            '#' => Some(Self::Infected),
            _ => None,
        }
    }
}

impl State {
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
    grid: HashMap<Point, State>,
    transitions: HashMap<State, State>,
    position: Point,
    direction: usize,
    directions: [Point; 4],
    infections: usize,
}

impl Virus {
    fn new(grid: HashMap<Point, State>, transitions: HashMap<State, State>) -> Self {
        let (mut x, mut y) = (0, 0);
        for point in grid.keys() {
            (x, y) = (x.max(point.0), y.max(point.1));
        }
        Self {
            grid,
            transitions,
            position: (x / 2, y / 2),
            direction: 0,
            directions: [(0, -1), (-1, 0), (0, 1), (1, 0)],
            infections: 0,
        }
    }

    fn burst(&mut self) {
        let state = self.grid.get(&self.position).unwrap_or(&State::Clean);
        self.direction = (self.direction + state.rotations()) % self.directions.len();
        let (dx, dy) = self.directions[self.direction];
        let new_state = self.transitions.get(state).unwrap();
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
    let lines = Reader::default().read_lines();
    let mut grid: HashMap<Point, State> = HashMap::default();
    for (y, line) in lines.iter().enumerate() {
        for (x, ch) in line.char_indices() {
            grid.insert((x as i16, y as i16), State::from_char(ch).unwrap());
        }
    }
    let simplified = HashMap::from_iter([
        (State::Clean, State::Infected),
        (State::Infected, State::Clean),
    ]);
    answer::part1(5575, run(&grid, 10_000, simplified));
    let expanded = HashMap::from_iter([
        (State::Clean, State::Weakened),
        (State::Weakened, State::Infected),
        (State::Infected, State::Flagged),
        (State::Flagged, State::Clean),
    ]);
    answer::part2(2511991, run(&grid, 10_000_000, expanded));
}

fn run(grid: &HashMap<Point, State>, n: usize, transitions: HashMap<State, State>) -> usize {
    let mut virus = Virus::new(grid.clone(), transitions);
    for _ in 0..n {
        virus.burst();
    }
    virus.infections
}
