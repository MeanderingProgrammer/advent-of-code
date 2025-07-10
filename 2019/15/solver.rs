use aoc::int_code::{Bus, Computer};
use aoc::prelude::*;
use std::collections::VecDeque;

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
    grid: HashMap<Point, Item>,
}

impl Default for RepairDroid {
    fn default() -> Self {
        Self {
            completed: false,
            position: Point::default(),
            next_position: None,
            // Initial direction to the origin does not matter it is never used
            path: [(Direction::Up, Point::default())].into(),
            grid: [(Point::default(), Item::Empty)].into_iter().collect(),
        }
    }
}

impl RepairDroid {
    fn get_unexplored(&self) -> Option<Direction> {
        Direction::values()
            .iter()
            .find(|&direction| !self.grid.contains_key(&self.position.add(direction)))
            .cloned()
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
            self.next_position = Some((direction.clone(), self.position.add(&direction)));
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
    grid: HashMap<Point, Item>,
}

impl GraphSearch for Search {
    type T = Point;

    fn first(&self) -> bool {
        true
    }

    fn done(&self, node: &Self::T) -> bool {
        self.grid.get(node).unwrap().is_oxygen()
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = Self::T> {
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
            .map(|(position, _)| self.dfs(position.clone()).first().cloned().unwrap())
            .max()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    let mut computer: Computer<RepairDroid> = Computer::default(&memory);
    computer.run();
    let search = Search {
        grid: computer.bus.grid,
    };
    answer::part1(224, search.dfs(Point::default()).first().cloned().unwrap());
    answer::part2(284, search.time_for_air().unwrap());
}
