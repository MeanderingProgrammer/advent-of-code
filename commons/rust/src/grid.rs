use crate::point::Point;
use fxhash::FxHashMap;
use itertools::{Itertools, MinMaxResult};
use std::cmp::PartialEq;
use std::string::ToString;

#[derive(Debug, Clone, PartialEq)]
pub struct Grid<T> {
    grid: FxHashMap<Point, T>,
}

impl<T> Default for Grid<T> {
    fn default() -> Self {
        Self {
            grid: FxHashMap::default(),
        }
    }
}

impl<T> Grid<T> {
    pub fn from_lines(lines: &[String], f: impl Fn(&Point, char) -> Option<T>) -> Self {
        let mut grid = Self::default();
        for (y, line) in lines.iter().enumerate() {
            for (x, ch) in line.char_indices() {
                let point = Point::new(x as i64, y as i64);
                if let Some(value) = f(&point, ch) {
                    grid.add(point, value);
                }
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

    pub fn values(&self) -> Vec<&T> {
        self.grid.values().collect()
    }

    pub fn height(&self) -> Option<i64> {
        self.points().iter().map(|point| point.y).max()
    }

    pub fn bounds(&self, buffer: i64) -> Bound {
        if self.grid.is_empty() {
            panic!("Can't get the bounds of an empty grid");
        }
        fn get_min_max(min_max: MinMaxResult<i64>, buffer: i64) -> (i64, i64) {
            match min_max {
                MinMaxResult::MinMax(min, max) => (min - buffer, max + buffer),
                _ => panic!("Could not find min max"),
            }
        }
        let (min_x, max_x) = get_min_max(self.grid.keys().map(|point| point.x).minmax(), buffer);
        let (min_y, max_y) = get_min_max(self.grid.keys().map(|point| point.y).minmax(), buffer);
        Bound {
            lower: Point::new(min_x, min_y),
            upper: Point::new(max_x, max_y),
        }
    }
}

impl<T> Grid<T>
where
    T: PartialEq,
{
    pub fn points_with_value(&self, target: T) -> Vec<&Point> {
        self.grid
            .iter()
            .filter(|(_, value)| value == &&target)
            .map(|(point, _)| point)
            .collect()
    }
}

impl<T> ToString for Grid<T>
where
    T: ToString,
{
    fn to_string(&self) -> String {
        if self.grid.is_empty() {
            return "".to_string();
        }
        let bounds = self.bounds(0);
        let (bottom_left, top_right) = (bounds.lower, bounds.upper);
        (bottom_left.y..=top_right.y)
            .map(|y| {
                (bottom_left.x..=top_right.x)
                    .map(|x| Point::new(x, y))
                    .map(|point| match self.get_or(&point) {
                        Some(value) => value.to_string(),
                        None => ".".to_string(),
                    })
                    .join("")
            })
            .join("\n")
    }
}

#[derive(Debug, Clone)]
pub struct Bound {
    pub lower: Point,
    pub upper: Point,
}

impl Bound {
    pub fn size(&self) -> i64 {
        let width = self.upper.x - self.lower.x + 1;
        let height = self.upper.y - self.lower.y + 1;
        width * height
    }

    pub fn contain(&self, point: &Point) -> bool {
        let contains_x = point.x >= self.lower.x && point.x <= self.upper.x;
        let contains_y = point.y >= self.lower.y && point.y <= self.upper.y;
        contains_x && contains_y
    }
}
