use std::cmp::Ordering;
use std::fmt;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "^" | "U" | "north" => Ok(Self::Up),
            ">" | "R" | "east" => Ok(Self::Right),
            "v" | "D" | "south" => Ok(Self::Down),
            "<" | "L" | "west" => Ok(Self::Left),
            _ => Err(format!("Unknown direction: {s}")),
        }
    }
}

impl From<&Direction> for Point {
    fn from(value: &Direction) -> Self {
        match value {
            Direction::Up => Self::new(0, -1),
            Direction::Down => Self::new(0, 1),
            Direction::Left => Self::new(-1, 0),
            Direction::Right => Self::new(1, 0),
        }
    }
}

impl Direction {
    pub fn from_char(ch: char) -> Option<Self> {
        match ch {
            '^' => Some(Self::Up),
            'v' => Some(Self::Down),
            '<' => Some(Self::Left),
            '>' => Some(Self::Right),
            _ => None,
        }
    }

    pub fn values() -> &'static [Self] {
        &[Self::Up, Self::Down, Self::Left, Self::Right]
    }

    pub fn left(&self) -> Self {
        match self {
            Self::Up => Self::Left,
            Self::Left => Self::Down,
            Self::Down => Self::Right,
            Self::Right => Self::Up,
        }
    }

    pub fn right(&self) -> Self {
        match self {
            Self::Up => Self::Right,
            Self::Right => Self::Down,
            Self::Down => Self::Left,
            Self::Left => Self::Up,
        }
    }

    pub fn opposite(&self) -> Self {
        match self {
            Self::Up => Self::Down,
            Self::Down => Self::Up,
            Self::Left => Self::Right,
            Self::Right => Self::Left,
        }
    }
}

#[derive(Debug)]
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

impl From<&Heading> for Point {
    fn from(value: &Heading) -> Self {
        match value {
            Heading::SouthEast => Self::new(1, 1),
            Heading::East => Self::new(1, 0),
            Heading::NorthEast => Self::new(1, -1),
            Heading::SouthWest => Self::new(-1, 1),
            Heading::West => Self::new(-1, 0),
            Heading::NorthWest => Self::new(-1, -1),
            Heading::South => Self::new(0, 1),
            Heading::North => Self::new(0, -1),
        }
    }
}

impl Heading {
    pub fn values() -> &'static [Self] {
        &[
            Self::SouthEast,
            Self::East,
            Self::NorthEast,
            Self::SouthWest,
            Self::West,
            Self::NorthWest,
            Self::South,
            Self::North,
        ]
    }
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
            .split(',')
            .map(|coord| coord.trim().parse().unwrap())
            .collect();
        if values.len() == 2 {
            Ok(Self::new(values[0], values[1]))
        } else {
            Err(format!("Unknown point format {s}"))
        }
    }
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
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

    pub fn add<P: Into<Self>>(&self, rhs: P) -> Self {
        let rhs: Self = rhs.into();
        Self::new(self.x + rhs.x, self.y + rhs.y)
    }

    pub fn sub<P: Into<Self>>(&self, rhs: P) -> Self {
        let rhs: Self = rhs.into();
        Self::new(self.x - rhs.x, self.y - rhs.y)
    }

    pub fn mul(&self, rhs: i64) -> Self {
        Self::new(self.x * rhs, self.y * rhs)
    }

    pub fn neighbors(&self) -> Vec<Self> {
        Direction::values()
            .iter()
            .map(|dir| self.add(dir))
            .collect()
    }

    pub fn diagonal_neighbors(&self) -> Vec<Self> {
        Heading::values()
            .iter()
            .map(|head| self.add(head))
            .collect()
    }

    pub fn distance(&self, other: &Self) -> f64 {
        let sum_squares = (self.x - other.x).pow(2) + (self.y - other.y).pow(2);
        (sum_squares as f64).sqrt()
    }

    pub fn manhattan_distance(&self, other: &Self) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }

    pub fn length(&self) -> i64 {
        self.x.abs() + self.y.abs()
    }
}

#[derive(Debug)]
pub enum Direction3d {
    Up,
    Down,
    Left,
    Right,
    Forward,
    Backward,
}

impl From<&Direction3d> for Point3d {
    fn from(value: &Direction3d) -> Self {
        match value {
            Direction3d::Up => Self::new(0, 0, 1),
            Direction3d::Down => Self::new(0, 0, -1),
            Direction3d::Forward => Self::new(0, 1, 0),
            Direction3d::Backward => Self::new(0, -1, 0),
            Direction3d::Left => Self::new(-1, 0, 0),
            Direction3d::Right => Self::new(1, 0, 0),
        }
    }
}

impl Direction3d {
    pub fn values() -> &'static [Self] {
        &[
            Self::Up,
            Self::Down,
            Self::Left,
            Self::Right,
            Self::Forward,
            Self::Backward,
        ]
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
            .split(',')
            .map(|coord| coord.trim().parse().unwrap())
            .collect();
        if values.len() == 3 {
            Ok(Self::new(values[0], values[1], values[2]))
        } else {
            Err(format!("Unknown point format {s}"))
        }
    }
}

impl fmt::Display for Point3d {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.z)
    }
}

impl Point3d {
    pub fn new(x: i64, y: i64, z: i64) -> Self {
        Self { x, y, z }
    }

    pub fn add<P: Into<Self>>(&self, rhs: P) -> Self {
        let rhs: Self = rhs.into();
        Self::new(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
    }

    pub fn sub<P: Into<Self>>(&self, rhs: P) -> Self {
        let rhs: Self = rhs.into();
        Self::new(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
    }

    pub fn mul(&self, rhs: i64) -> Self {
        Self::new(self.x * rhs, self.y * rhs, self.z * rhs)
    }

    pub fn neighbors(&self) -> Vec<Self> {
        Direction3d::values()
            .iter()
            .map(|dir| self.add(dir))
            .collect()
    }

    pub fn length(&self) -> i64 {
        self.x.abs() + self.y.abs() + self.z.abs()
    }
}
