use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;
use fxhash::{FxHashMap, FxHashSet};
use std::collections::{BTreeMap, VecDeque};

const HALLWAY: i64 = 1;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
enum Value {
    Hallway,
    Doorway,
    A,
    B,
    C,
    D,
}

impl From<&Point> for Value {
    fn from(point: &Point) -> Self {
        let alley = match point.x {
            3 => Self::A,
            5 => Self::B,
            7 => Self::C,
            9 => Self::D,
            _ => Self::Hallway,
        };
        if point.y == HALLWAY && alley != Self::Hallway {
            Self::Doorway
        } else {
            alley
        }
    }
}

impl Value {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            'A' => Some(Self::A),
            'B' => Some(Self::B),
            'C' => Some(Self::C),
            'D' => Some(Self::D),
            _ => None,
        }
    }

    fn x(&self) -> i64 {
        match self {
            Self::A => Some(3),
            Self::B => Some(5),
            Self::C => Some(7),
            Self::D => Some(9),
            _ => None,
        }
        .unwrap()
    }

    fn cost(&self) -> Option<i64> {
        match self {
            Self::A => Some(1),
            Self::B => Some(10),
            Self::C => Some(100),
            Self::D => Some(1000),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Pod {
    value: Value,
    start: bool,
}

impl Pod {
    fn new(value: Value) -> Self {
        Self { value, start: true }
    }

    fn done(&self, p: &Point) -> bool {
        self.value.x() == p.x
    }

    fn crosses(&self, x1: i64) -> impl Iterator<Item = i64> {
        let x2 = self.value.x();
        x1.min(x2) + 1..x1.max(x2)
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct State {
    pods: BTreeMap<Point, Pod>,
}

impl State {
    fn apply(&self, start: &Point, end: Point) -> (Self, i64) {
        let mut pods = self.pods.clone();
        let mut pod = pods.remove(start).unwrap();

        let cost = pod.value.cost().unwrap();
        // Movement along x-axis work as usual. However, along the y-axis we need
        // to go up to the hallway, then back down to our desired level.
        // So if the hallway is at y = 1, and we move from y = 4 to y = 2, what
        // really happens is we go from 4 -> 1 then 1 -> 2.
        let distance = (start.x - end.x).abs() + (start.y - HALLWAY) + (end.y - HALLWAY);

        pod.start = false;
        pods.insert(end, pod);

        (Self { pods }, cost * distance)
    }

    fn room(&self, x: i64) -> Option<i64> {
        let mut count = 0;
        for (point, pod) in self.pods.iter() {
            if point.x == x {
                if pod.value.x() != x {
                    return None;
                } else {
                    count += 1;
                }
            }
        }
        Some(count)
    }
}

#[derive(Debug)]
struct Board {
    graph: FxHashMap<Point, Vec<Point>>,
    size: i64,
}

impl Dijkstra for Board {
    type T = State;

    fn done(&self, state: &State) -> bool {
        state.pods.iter().all(|(point, pod)| pod.done(point))
    }

    fn neighbors(&self, state: &State) -> impl Iterator<Item = (State, i64)> {
        state
            .pods
            .iter()
            .filter(|(start, pod)| !pod.done(start) || pod.start)
            .flat_map(|(start, _)| {
                self.options(state, start)
                    .into_iter()
                    .map(|end| state.apply(start, end))
            })
    }
}

impl Board {
    fn options(&self, state: &State, start: &Point) -> Vec<Point> {
        let pod = &state.pods[start];
        let valid_rooms = [start.x, pod.value.x()];

        let mut seen = FxHashSet::default();
        let mut options = Vec::new();

        let mut queue = VecDeque::new();
        queue.push_back(start.clone());
        while let Some(end) = queue.pop_back() {
            let in_room = end.y != HALLWAY;

            // Prune branches going into invalid rooms
            if in_room && !valid_rooms.contains(&end.x) {
                continue;
            }

            if seen.contains(&end) {
                continue;
            }
            seen.insert(end.clone());

            if self.valid(state, pod, &end) {
                if in_room {
                    // If we can get into the room pick this move
                    return vec![end];
                } else {
                    options.push(end.clone());
                }
            }

            for next in &self.graph[&end] {
                if !state.pods.contains_key(next) {
                    queue.push_back(next.clone());
                }
            }
        }
        options
    }

    fn valid(&self, state: &State, pod: &Pod, end: &Point) -> bool {
        let end_value = end.into();
        match end_value {
            // Never stop outside of a room
            Value::Doorway => false,
            Value::Hallway => {
                if !pod.start {
                    // Can not move to hallway once we have already been moved
                    false
                } else {
                    // Here we detect "deadlock", which occurs when we put our amphipod
                    // in the Hallway and this blocks an amphipod from reaching their
                    // room who is in turn blocking us
                    pod.crosses(end.x).all(|x| {
                        state
                            .pods
                            .get(&Point::new(x, HALLWAY))
                            .map(|o| !o.crosses(x).any(|o_x| o_x == end.x))
                            .unwrap_or(true)
                    })
                }
            }
            _ => {
                if pod.value != end_value {
                    // If this room is for another amphipod then we cannot enter
                    false
                } else {
                    // Must be the room for this amphipod, need to make sure that:
                    // 1) Only valid amphipods are in the room
                    // 2) We go to the correct point in the room, as far back as possible
                    match state.room(pod.value.x()) {
                        None => false,
                        Some(count) => end.y == self.size + HALLWAY - count,
                    }
                }
            }
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().read_lines();
    answer::part1(18282, solve(&data, false));
    answer::part2(50132, solve(&data, true));
}

fn solve(lines: &[String], extend: bool) -> i64 {
    let rows = get_rows(lines, extend);
    let board = get_board(&rows);
    let state = get_state(&rows);
    board.run(state).unwrap()
}

fn get_rows(rows: &[String], extend: bool) -> Vec<String> {
    let mut result = Vec::from(rows);
    if extend {
        let last_row = result.pop().unwrap();
        let second_last_row = result.pop().unwrap();
        result.extend([
            "  #D#C#B#A#".to_string(),
            "  #D#B#A#C#".to_string(),
            second_last_row,
            last_row,
        ]);
    }
    result
}

fn get_board(rows: &[String]) -> Board {
    let grid = Grid::from_lines(rows, |_, ch| match ch {
        '#' | ' ' => None,
        _ => Some(ch),
    });
    Board {
        graph: grid.to_graph(),
        size: grid.bounds().upper.y - 1,
    }
}

fn get_state(rows: &[String]) -> State {
    let grid = Grid::from_lines(rows, |_, ch| Value::from_char(ch).map(Pod::new));
    State {
        pods: grid
            .points()
            .into_iter()
            .map(|point| (point.clone(), grid.get(point).clone()))
            .collect(),
    }
}
