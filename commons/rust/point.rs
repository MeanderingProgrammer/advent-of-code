use std::cmp::Ordering;
use std::ops::{Add, Mul};
use std::str::FromStr;
use strum::IntoEnumIterator;
use strum_macros::EnumIter;

#[derive(Debug, EnumIter, Clone, PartialEq, Eq, Hash)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    pub fn to_point(&self) -> Point {
        match self {
            Self::Up => Point::new(0, -1),
            Self::Down => Point::new(0, 1),
            Self::Left => Point::new(-1, 0),
            Self::Right => Point::new(1, 0),
        }
    }
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

impl Heading {
    pub fn to_point(&self) -> Point {
        match self {
            Self::SouthEast => Point::new(1, 1),
            Self::East => Point::new(1, 0),
            Self::NorthEast => Point::new(1, -1),
            Self::SouthWest => Point::new(-1, 1),
            Self::West => Point::new(-1, 0),
            Self::NorthWest => Point::new(-1, -1),
            Self::South => Point::new(0, 1),
            Self::North => Point::new(0, -1),
        }
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

impl Add for &Point {
    type Output = Point;

    fn add(self, rhs: &Point) -> Point {
        Point {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

impl Add<&Direction> for &Point {
    type Output = Point;

    fn add(self, rhs: &Direction) -> Point {
        self + &rhs.to_point()
    }
}

impl Add<&Heading> for &Point {
    type Output = Point;

    fn add(self, rhs: &Heading) -> Point {
        self + &rhs.to_point()
    }
}

impl Mul<i64> for &Point {
    type Output = Point;

    fn mul(self, rhs: i64) -> Point {
        Point {
            x: self.x * rhs,
            y: self.y * rhs,
        }
    }
}

impl Point {
    pub fn new(x: i64, y: i64) -> Self {
        Self { x, y }
    }

    pub fn neighbors(&self) -> Vec<Self> {
        Direction::iter().map(|dir| self + &dir).collect()
    }

    pub fn diagonal_neighbors(&self) -> Vec<Self> {
        Heading::iter().map(|heading| self + &heading).collect()
    }

    pub fn distance(&self, other: &Self) -> f64 {
        let sum_squares = (self.x - other.x).pow(2) + (self.y - other.y).pow(2);
        (sum_squares as f64).sqrt()
    }

    pub fn manhattan_distance(&self, other: &Self) -> i64 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }
}

#[derive(Debug, EnumIter)]
pub enum Direction3d {
    Up,
    Down,
    Left,
    Right,
    Forward,
    Backward,
}

impl Direction3d {
    pub fn to_point(&self) -> Point3d {
        match self {
            Self::Up => Point3d::new(0, 0, 1),
            Self::Down => Point3d::new(0, 0, -1),
            Self::Forward => Point3d::new(0, 1, 0),
            Self::Backward => Point3d::new(0, -1, 0),
            Self::Left => Point3d::new(-1, 0, 0),
            Self::Right => Point3d::new(1, 0, 0),
        }
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

impl Add for &Point3d {
    type Output = Point3d;

    fn add(self, rhs: &Point3d) -> Point3d {
        Point3d {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z,
        }
    }
}

impl Add<&Direction3d> for &Point3d {
    type Output = Point3d;

    fn add(self, rhs: &Direction3d) -> Point3d {
        self + &rhs.to_point()
    }
}

impl Point3d {
    pub fn new(x: i64, y: i64, z: i64) -> Self {
        Self { x, y, z }
    }

    pub fn neighbors(&self) -> Vec<Self> {
        Direction3d::iter().map(|dir| self + &dir).collect()
    }
}
