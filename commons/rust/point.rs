use std::cmp::Ordering;
use std::str::FromStr;
use strum_macros::EnumIter;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug, EnumIter)]
pub enum Heading {
    SouthEast,
    East,
    NorthEast,
    SouthWest,
    West,
    NorthWest,
    South,
    North,
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
pub struct Point {
    pub x: i64,
    pub y: i64,
}

impl FromStr for Point {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let values: Vec<i64> = s
            .split(",")
            .map(|coord| coord.trim().parse().unwrap())
            .collect();
        if values.len() == 2 {
            Ok(Self::new(values[0], values[1]))
        } else {
            Err(format!("Unknown point format {s}"))
        }
    }
}

impl ToString for Point {
    fn to_string(&self) -> String {
        format!("({}, {})", self.x, self.y)
    }
}

impl Ord for Point {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.y, self.x).cmp(&(other.y, other.x))
    }
}

impl PartialOrd for Point {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Point {
    pub fn new(x: i64, y: i64) -> Self {
        Self { x, y }
    }

    pub fn add(&self, dx: i64, dy: i64) -> Self {
        Self {
            x: self.x + dx,
            y: self.y + dy,
        }
    }

    pub fn step_n(&self, direction: &Direction, n: i64) -> Self {
        match direction {
            Direction::Up => self.add(0, -n),
            Direction::Down => self.add(0, n),
            Direction::Left => self.add(-n, 0),
            Direction::Right => self.add(n, 0),
        }
    }

    pub fn step(&self, direction: &Direction) -> Self {
        self.step_n(direction, 1)
    }

    pub fn neighbors(&self) -> Vec<Self> {
        vec![
            self.add(0, -1),
            self.add(0, 1),
            self.add(-1, 0),
            self.add(1, 0),
        ]
    }

    pub fn head(&self, heading: &Heading) -> Self {
        match heading {
            Heading::SouthEast => self.add(1, 1),
            Heading::East => self.add(1, 0),
            Heading::NorthEast => self.add(1, -1),
            Heading::SouthWest => self.add(-1, 1),
            Heading::West => self.add(-1, 0),
            Heading::NorthWest => self.add(-1, -1),
            Heading::South => self.add(0, 1),
            Heading::North => self.add(0, -1),
        }
    }

    pub fn diagonal_neighbors(&self) -> Vec<Self> {
        vec![
            self.add(1, 1),
            self.add(1, 0),
            self.add(1, -1),
            self.add(-1, 1),
            self.add(-1, 0),
            self.add(-1, -1),
            self.add(0, 1),
            self.add(0, -1),
        ]
    }

    pub fn distance(&self, other: &Self) -> f64 {
        let sum_squares = (self.x - other.x).pow(2) + (self.y - other.y).pow(2);
        (sum_squares as f64).sqrt()
    }

    pub fn manhattan_distance(&self, other: &Self) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
pub struct Point3d {
    pub x: i64,
    pub y: i64,
    pub z: i64,
}

impl FromStr for Point3d {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let values: Vec<i64> = s
            .split(",")
            .map(|coord| coord.trim().parse().unwrap())
            .collect();
        if values.len() == 3 {
            Ok(Self::new(values[0], values[1], values[2]))
        } else {
            Err(format!("Unknown point format {s}"))
        }
    }
}

impl ToString for Point3d {
    fn to_string(&self) -> String {
        format!("({}, {}, {})", self.x, self.y, self.z)
    }
}

impl Point3d {
    pub fn new(x: i64, y: i64, z: i64) -> Self {
        Self { x, y, z }
    }

    pub fn add(&self, dx: i64, dy: i64, dz: i64) -> Self {
        Self {
            x: self.x + dx,
            y: self.y + dy,
            z: self.z + dz,
        }
    }

    pub fn neighbors(&self) -> Vec<Self> {
        vec![
            self.add(1, 0, 0),
            self.add(-1, 0, 0),
            self.add(0, 1, 0),
            self.add(0, -1, 0),
            self.add(0, 0, 1),
            self.add(0, 0, -1),
        ]
    }
}
