use crate::point::Point;
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
    pub fn new() -> Grid<T> {
        Grid {
            grid: HashMap::new(),
        }
    }

    pub fn add(&mut self, point: Point, value: T) {
        self.grid.insert(point, value);
    }

    pub fn get(&self, point: &Point) -> &T {
        self.grid.get(point).unwrap()
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
}

impl<T: GridValue> fmt::Display for Grid<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (bottom_left, top_right) = self.bounds();

        let mut rows = Vec::new();
        for y in bottom_left.y()..=top_right.y() {
            let mut row = "".to_string();
            for x in bottom_left.x()..=top_right.x() {
                let point = Point::new_2d(x, y);
                if self.contains(&point) {
                    let as_string = self.get(&point).to_string();
                    row.push_str(&format!("[{}]", as_string));
                } else {
                    row += ".";
                }
            }
            rows.push(row);
        }

        write!(f, "{}", rows.join("\n"))
    }
}
