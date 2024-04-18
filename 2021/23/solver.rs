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

    fn from_point(point: &Point) -> Self {
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

    fn cost(&self) -> i64 {
        match self {
            Self::A => Some(1),
            Self::B => Some(10),
            Self::C => Some(100),
            Self::D => Some(1000),
            _ => None,
        }
        .unwrap()
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Character {
    value: Value,
    moved: bool,
}

impl Character {
    fn new(value: Value) -> Self {
        Self {
            value,
            moved: false,
        }
    }

    fn at_goal(&self, p: &Point) -> bool {
        self.value.x() == p.x
    }

    fn hallway_to_goal(&self, x1: i64) -> impl Iterator<Item = i64> {
        x1.min(self.value.x()) + 1..x1.max(self.value.x())
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct State {
    characters: BTreeMap<Point, Character>,
}

impl State {
    fn apply(&self, start: &Point, end: Point) -> (Self, i64) {
        let mut result = self.characters.clone();

        let mut character = result.remove(start).unwrap();
        character.moved = true;

        let cost = character.value.cost();
        // Movements along x-axis work as usual. However, along the y-axis we know we
        // need to go up to the Hallway, then back down to our desired level.
        // So if the hallway is at y = 1, and we move from y = 4 to y = 2, what really
        // happens is we go from 4 -> 1, then 1 -> 2.
        let distance = (start.x - end.x).abs() + (start.y - HALLWAY) + (end.y - HALLWAY);

        result.insert(end, character);

        (State { characters: result }, cost * distance)
    }

    fn destinations(&self, board: &Board, start: &Point) -> Vec<Point> {
        let character = &self.characters[start];

        let mut queue = VecDeque::new();
        queue.push_back(start.clone());
        let mut seen = FxHashSet::default();

        let mut destinations = Vec::new();
        while let Some(destination) = queue.pop_back() {
            if seen.contains(&destination) {
                continue;
            }
            seen.insert(destination.clone());

            let valid = self.valid(character, &destination, board.room_size);
            if valid {
                if destination.y > HALLWAY {
                    // If we can get into the room always pick just this move
                    return vec![destination];
                } else {
                    destinations.push(destination.clone());
                }
            }

            for adjacent in &board.graph[&destination] {
                if !self.characters.contains_key(adjacent) {
                    queue.push_back(adjacent.clone());
                }
            }
        }
        destinations
    }

    fn valid(&self, character: &Character, end: &Point, room_size: i64) -> bool {
        let end_value = Value::from_point(end);
        match end_value {
            // Can never stop outside of a room
            Value::Doorway => false,
            Value::Hallway => {
                if character.moved {
                    // Can not move to hallway once we have already been moved
                    false
                } else {
                    // Here we detect "deadlock", which occurs when we put our character in the Hallway
                    // and this blocks a character from reaching their room who is in turn blocking us
                    character.hallway_to_goal(end.x).all(|x| {
                        self.characters
                            .get(&Point { x, y: HALLWAY })
                            .map(|other| !other.hallway_to_goal(x).any(|value| value == end.x))
                            .unwrap_or(true)
                    })
                }
            }
            _ => {
                if character.value != end_value {
                    // If this room is for another character then we cannot enter
                    false
                } else {
                    // Otherwise it is the room for this character, we need to make sure that:
                    // 1) Only valid characters are in the room
                    // 2) That we go to the correct point in the room, i.e. as far back as possible
                    let in_room = self.in_room(&character.value);
                    let num_in_room = in_room.len() as i64;
                    let need_to_wait = in_room.into_iter().any(|other| other != &character.value);
                    if need_to_wait {
                        // At least one character in the room needs to leave
                        false
                    } else {
                        end.y == room_size - num_in_room + 1
                    }
                }
            }
        }
    }

    fn in_room(&self, value: &Value) -> Vec<&Value> {
        self.characters
            .iter()
            .filter_map(|(point, character)| {
                if point.x == value.x() {
                    Some(&character.value)
                } else {
                    None
                }
            })
            .collect()
    }
}

#[derive(Debug)]
struct Board {
    graph: FxHashMap<Point, Vec<Point>>,
    room_size: i64,
}

impl Dijkstra for Board {
    type T = State;
    type P = i64;

    fn done(&self, state: &State) -> bool {
        state
            .characters
            .iter()
            .all(|(point, character)| character.at_goal(point))
    }

    fn neighbors(&self, state: &State, weight: i64) -> impl Iterator<Item = (State, i64)> {
        state
            .characters
            .iter()
            .filter(|(point, character)| !character.at_goal(point) || !character.moved)
            .flat_map(|(start, _)| {
                state
                    .destinations(self, start)
                    .into_iter()
                    .map(|end| state.apply(start, end))
            })
            .map(move |(adjacent, cost)| (adjacent, weight + cost))
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
    board.run_min(state, 0).unwrap()
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
        room_size: grid.bounds().upper.y - 1,
    }
}

fn get_state(rows: &[String]) -> State {
    let grid = Grid::from_lines(rows, |_, ch| Value::from_char(ch).map(Character::new));
    State {
        characters: grid
            .points()
            .into_iter()
            .map(|point| (point.clone(), grid.get(point).clone()))
            .collect(),
    }
}
