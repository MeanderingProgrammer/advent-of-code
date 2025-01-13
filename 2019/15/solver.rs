use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::GraphSearch;
use fxhash::FxHashMap;
use std::collections::VecDeque;
use strum::IntoEnumIterator;

#[derive(Debug, Clone)]
enum Item {
    Wall,
    Empty,
    Oxygen,
}

impl Item {
    fn from_value(value: i64) -> Option<Self> {
        match value {
            0 => Some(Self::Wall),
            1 => Some(Self::Empty),
            2 => Some(Self::Oxygen),
            _ => None,
        }
    }

    fn is_open(&self) -> bool {
        match self {
            Self::Wall => false,
            Self::Empty | Self::Oxygen => true,
        }
    }

    fn is_oxygen(&self) -> bool {
        match self {
            Self::Oxygen => true,
            Self::Empty | Self::Wall => false,
        }
    }

    fn is_empty(&self) -> bool {
        match self {
            Self::Empty => true,
            Self::Oxygen | Self::Wall => false,
        }
    }
}

#[derive(Debug)]
struct RepairDroid {
    completed: bool,
    position: Point,
    next_position: Option<(Direction, Point)>,
    path: VecDeque<(Direction, Point)>,
    grid: FxHashMap<Point, Item>,
}

impl RepairDroid {
    fn new() -> Self {
        Self {
            completed: false,
            position: Point::default(),
            next_position: None,
            // Initial direction to the origin does not matter it is never used
            path: [(Direction::Up, Point::default())].into(),
            grid: [(Point::default(), Item::Empty)].into_iter().collect(),
        }
    }

    fn get_unexplored(&self) -> Option<Direction> {
        Direction::iter().find(|direction| !self.grid.contains_key(&(&self.position + direction)))
    }

    fn get_code(direction: &Direction) -> i64 {
        match direction {
            Direction::Down => 1,
            Direction::Up => 2,
            Direction::Left => 3,
            Direction::Right => 4,
        }
    }
}

impl Bus for RepairDroid {
    fn active(&self) -> bool {
        !self.completed
    }

    fn get_input(&mut self) -> i64 {
        if let Some(direction) = self.get_unexplored() {
            self.next_position = Some((direction.clone(), &self.position + &direction));
            Self::get_code(&direction)
        } else if self.path.len() > 1 {
            let (previous, _) = self.path.pop_back().unwrap();
            self.next_position = self.path.pop_back();
            Self::get_code(&previous.opposite())
        } else {
            self.completed = true;
            0
        }
    }

    fn add_output(&mut self, value: i64) {
        let item = Item::from_value(value).unwrap();
        let (direction, position) = self.next_position.clone().unwrap();
        self.grid.insert(position.clone(), item.clone());
        if item.is_open() {
            self.position = position.clone();
            self.path.push_back((direction, position));
        }
    }
}

#[derive(Debug)]
struct Search {
    grid: FxHashMap<Point, Item>,
}

impl GraphSearch for Search {
    type T = Point;

    fn first(&self) -> bool {
        true
    }

    fn done(&self, node: &Point) -> bool {
        self.grid.get(node).unwrap().is_oxygen()
    }

    fn neighbors(&self, node: &Point) -> impl Iterator<Item = Point> {
        node.neighbors()
            .into_iter()
            .filter(|neighbor| self.grid.get(neighbor).unwrap_or(&Item::Wall).is_open())
    }
}

impl Search {
    fn time_for_air(&self) -> Option<i64> {
        self.grid
            .iter()
            .filter(|(_, value)| value.is_empty())
            .map(|(position, _)| self.bfs(position.clone()).first().cloned().unwrap())
            .max()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut computer = Computer::new(RepairDroid::new(), Reader::default().read_csv());
    computer.run();
    let search = Search {
        grid: computer.bus.grid,
    };
    answer::part1(224, search.bfs(Point::default()).first().cloned().unwrap());
    answer::part2(284, search.time_for_air().unwrap());
}
