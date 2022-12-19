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

    pub fn bounds(&self) -> (Point, Point) {
        let points = self.points();        
        (
            Point::new_2d(
                points.iter().map(|p| p.x()).min().unwrap(), 
                points.iter().map(|p| p.y()).min().unwrap(),
            ), 
            Point::new_2d(
                points.iter().map(|p| p.x()).max().unwrap(), 
                points.iter().map(|p| p.y()).max().unwrap(),
            ),
        )
    }

    pub fn as_string(&self, buffer: i64) -> String {
        if self.grid.len() == 0 {
            return "".to_string();
        }

        let (bottom_left, top_right) = self.bounds();
        (bottom_left.y()-buffer..=top_right.y()+buffer)
            .map(|y| (bottom_left.x()-buffer..=top_right.x()+buffer)
                .map(|x| Point::new_2d(x, y))
                .map(|point| match self.get_or(&point) {
                    Some(value) => value.to_string(),
                    None => String::from("."),
                })
                .join("")
            )
            .join("\n")
    }
}

impl<T: GridValue> fmt::Display for Grid<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.as_string(0))
    }
}
