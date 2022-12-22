use crate::point::Point;
use itertools::Itertools;
use std::cmp::PartialEq;
use std::collections::HashMap;
use std::fmt;
use std::string::ToString;

pub trait GridValue: PartialEq + ToString {}
impl<T: PartialEq + ToString> GridValue for T {}

#[derive(Debug)]
pub struct Grid<T: GridValue> {
    grid: HashMap<Point, T>,
}

impl<T: GridValue> Grid<T> {
    pub fn new() -> Self {
        Grid {
            grid: HashMap::new(),
        }
    }

    pub fn from_lines(lines: Vec<String>, f : impl Fn(char) -> Option<T>) -> Self {
        let mut grid = Self::new();
        for (y, line) in lines.iter().enumerate() {
            for (x, ch) in line.char_indices() {
                let point = Point::new_2d(x as i64, y as i64);
                match f(ch) {
                    Some(value) => grid.add(point, value),
                    None => (),
                };
            }
        }
        grid
    }

    pub fn add(&mut self, point: Point, value: T) {
        self.grid.insert(point, value);
    }

    pub fn remove(&mut self, point: &Point) {
        self.grid.remove(point);
    }

    pub fn get(&self, point: &Point) -> &T {
        self.grid.get(point).unwrap()
    }

    pub fn get_or(&self, point: &Point) -> Option<&T> {
        self.grid.get(point)
    }

    pub fn contains(&self, point: &Point) -> bool {
        self.grid.contains_key(point)
    }

    pub fn points(&self) -> Vec<&Point> {
        self.grid.keys().collect()
    }

    pub fn points_with_value(&self, target: T) -> Vec<&Point> {
        self.grid.iter()
            .filter(|(_, value)| value == &&target)
            .map(|(point, _)| point)
            .collect()
    }

    pub fn height(&self) -> Option<i64> {
        self.points().iter()
            .map(|point| point.y())
            .max()
    }

    pub fn bounds(&self, buffer: i64) -> Bound {
        let points = self.points();
        if points.len() == 0 {
            panic!("Can't get the bounds of an empty grid");
        }

        let mut mins = Vec::new();
        let mut maxs = Vec::new();
        for i in 0..points[0].dimensions() {
            mins.push(points.iter().map(|point| point.get(i)).min().unwrap() - buffer);
            maxs.push(points.iter().map(|point| point.get(i)).max().unwrap() + buffer);
        }

        Bound {
            lower: Point::new_nd(mins),
            upper: Point::new_nd(maxs),
        }
    }

    pub fn as_string(&self, default: &str, buffer: i64) -> String {
        if self.grid.len() == 0 {
            return "".to_string();
        }

        let bounds = self.bounds(buffer);
        let (bottom_left, top_right) = (bounds.lower, bounds.upper);
        (bottom_left.y()..=top_right.y())
            .map(|y| (bottom_left.x()..=top_right.x())
                .map(|x| Point::new_2d(x, y))
                .map(|point| match self.get_or(&point) {
                    Some(value) => value.to_string(),
                    None => String::from(default),
                })
                .join("")
            )
            .join("\n")
    }
}

impl<T: GridValue> fmt::Display for Grid<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_string(".", 0))
    }
}

#[derive(Debug)]
pub struct Bound {
    lower: Point,
    upper: Point,
}

impl Bound {
    pub fn lower(&self) -> &Point {
        &self.lower
    }

    pub fn upper(&self) -> &Point {
        &self.upper
    }

    pub fn contain(&self, point: &Point) -> bool {
        (0..point.dimensions())
            .all(|i| {
                let value = point.get(i);
                value >= self.lower.get(i) && value <= self.upper.get(i)
            })
    }
}
