use crate::{FromChar, HashMap, Iter, Point};
use std::borrow::Borrow;
use std::cmp::PartialEq;
use std::fmt;
use std::ops::Index;
use std::string::ToString;

#[derive(Debug, Clone, PartialEq)]
pub struct Grid<T> {
    grid: HashMap<Point, T>,
}

impl<T> Default for Grid<T> {
    fn default() -> Self {
        Self {
            grid: HashMap::default(),
        }
    }
}

impl<T> From<&str> for Grid<T>
where
    T: FromChar,
{
    fn from(value: &str) -> Self {
        (&value.lines().collect::<Vec<_>>()).into()
    }
}

impl<T, S> From<&Vec<S>> for Grid<T>
where
    T: FromChar,
    S: AsRef<str>,
{
    fn from(value: &Vec<S>) -> Self {
        let mut grid = Self::default();
        for (y, line) in value.iter().enumerate() {
            for (x, ch) in line.as_ref().char_indices() {
                let point = Point::new(x as i32, y as i32);
                if let Some(value) = T::from_char(ch) {
                    grid.add(point, value);
                }
            }
        }
        grid
    }
}

impl<T> Grid<T> {
    pub fn add(&mut self, point: Point, value: T) {
        self.grid.insert(point, value);
    }

    pub fn remove(&mut self, point: &Point) {
        self.grid.remove(point);
    }

    pub fn get(&self, point: &Point) -> Option<&T> {
        self.grid.get(point)
    }

    pub fn has(&self, point: &Point) -> bool {
        self.grid.contains_key(point)
    }

    pub fn iter(&self) -> impl Iterator<Item = (&Point, &T)> {
        self.grid.iter()
    }

    pub fn bounds(&self) -> Bounds {
        let points: Vec<&Point> = self.grid.keys().collect();
        Bounds::new(&points)
    }

    pub fn to_graph(&self) -> HashMap<Point, Vec<Point>> {
        self.iter()
            .map(|(point, _)| {
                let neighbors = point
                    .neighbors()
                    .into_iter()
                    .filter(|neighbor| self.has(neighbor))
                    .collect();
                (point.clone(), neighbors)
            })
            .collect()
    }
}

impl<T> Index<&Point> for Grid<T> {
    type Output = T;

    fn index(&self, index: &Point) -> &Self::Output {
        &self.grid[index]
    }
}

impl<T> Grid<T>
where
    T: PartialEq,
{
    pub fn is(&self, point: &Point, target: &T) -> bool {
        match self.get(point) {
            None => false,
            Some(value) => value == target,
        }
    }

    pub fn values(&self, target: &T) -> Vec<Point> {
        self.iter()
            .filter(|(_, value)| value == &target)
            .map(|(point, _)| point.clone())
            .collect()
    }

    pub fn value(&self, target: &T) -> Point {
        let mut values = self.values(target);
        assert_eq!(1, values.len());
        values.pop().unwrap()
    }
}

impl<T> Grid<T>
where
    T: Clone,
{
    pub fn get_or(&self, point: &Point, default: T) -> T {
        self.get(point).cloned().unwrap_or(default)
    }

    pub fn transform(&self, f: impl Fn(&Point) -> Point) -> Self {
        let mut result = Self::default();
        for (point, value) in self.grid.iter() {
            result.add(f(point), value.clone());
        }
        result
    }
}

impl<T> fmt::Display for Grid<T>
where
    T: ToString,
{
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let value = if self.grid.is_empty() {
            "".to_string()
        } else {
            let bounds = self.bounds();
            let (bottom_left, top_right) = (bounds.lower, bounds.upper);
            (bottom_left.y..=top_right.y)
                .map(|y| {
                    (bottom_left.x..=top_right.x)
                        .map(|x| Point::new(x, y))
                        .map(|point| match self.get(&point) {
                            None => ".".to_string(),
                            Some(value) => value.to_string(),
                        })
                        .join("")
                })
                .join("\n")
        };
        write!(f, "{}", value)
    }
}

#[derive(Debug, Clone)]
pub struct Bounds {
    pub lower: Point,
    pub upper: Point,
}

impl Bounds {
    pub fn new<T: Borrow<Point>>(points: &[T]) -> Bounds {
        let points: Vec<&Point> = points.iter().map(|point| point.borrow()).collect();
        if points.is_empty() {
            panic!("Can't get the bounds of an empty area");
        }
        let (min_x, max_x) = points.iter().map(|point| point.x).minmax().unwrap();
        let (min_y, max_y) = points.iter().map(|point| point.y).minmax().unwrap();
        Self {
            lower: Point::new(min_x, min_y),
            upper: Point::new(max_x, max_y),
        }
    }

    pub fn size(&self) -> i64 {
        let width = self.upper.x - self.lower.x + 1;
        let height = self.upper.y - self.lower.y + 1;
        (width as i64) * (height as i64)
    }

    pub fn contain(&self, point: &Point) -> bool {
        let contains_x = point.x >= self.lower.x && point.x <= self.upper.x;
        let contains_y = point.y >= self.lower.y && point.y <= self.upper.y;
        contains_x && contains_y
    }

    pub fn edge(&self, point: &Point) -> bool {
        let edge_x = point.x == self.lower.x || point.x == self.upper.x;
        let edge_y = point.y == self.lower.y || point.y == self.upper.y;
        edge_x || edge_y
    }
}
