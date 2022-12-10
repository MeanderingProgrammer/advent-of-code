use crate::point::Point;
use std::collections::HashMap;

#[derive(Debug)]
pub struct Grid<T> {
    grid: HashMap<Point, T>,
}

impl<T> Grid<T> {
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
}
