use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Point {
    values: Vec<i64>,
}

impl Ord for Point {
    fn cmp(&self, other: &Self) -> Ordering {
        let self_values: Vec<&i64> = self.values.iter().rev().collect();
        let other_values: Vec<&i64> = other.values.iter().rev().collect();
        self_values.cmp(&other_values)
    }
}

impl PartialOrd for Point {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Point {
    pub fn new(dimensions: usize) -> Point {
        Point {
            values: vec![0; dimensions],
        }
    }

    pub fn new_2d(x: i64, y: i64) -> Point {
        Point { values: vec![x, y] }
    }

    pub fn new_nd(values: Vec<i64>) -> Point {
        Point { values }
    }

    pub fn dimensions(&self) -> usize {
        self.values.len()
    }

    pub fn x(&self) -> i64 {
        self.get(0)
    }

    pub fn y(&self) -> i64 {
        self.get(1)
    }

    pub fn z(&self) -> i64 {
        self.get(2)
    }

    pub fn get(&self, index: usize) -> i64 {
        self.check_index(index);
        self.values[index]
    }

    pub fn add_x(&self, value: i64) -> Self {
        self.add(0, value)
    }

    pub fn add_y(&self, value: i64) -> Self {
        self.add(1, value)
    }

    pub fn add_z(&self, value: i64) -> Self {
        self.add(2, value)
    }

    fn add(&self, index: usize, value: i64) -> Self {
        self.check_index(index);
        let mut copied = self.values.clone();
        copied[index] += value;
        Point { values: copied }
    }

    pub fn neighbors(&self) -> Vec<Self> {
        match self.dimensions() {
            2 => vec![self.add_x(1), self.add_x(-1), self.add_y(1), self.add_y(-1)],
            3 => vec![
                self.add_x(1),
                self.add_x(-1),
                self.add_y(1),
                self.add_y(-1),
                self.add_z(1),
                self.add_z(-1),
            ],
            _ => panic!("Unsupported number of dimensions for computing neighbors"),
        }
    }

    pub fn distance(&self, other: &Self) -> f64 {
        self.check_dimension(other);
        let mut sum_squares = 0;
        for i in 0..self.dimensions() {
            let diff = self.get(i) - other.get(i);
            sum_squares += diff.pow(2);
        }
        (sum_squares as f64).sqrt()
    }

    pub fn manhattan_distance(&self, other: &Self) -> i64 {
        self.check_dimension(other);
        let mut distance = 0;
        for i in 0..self.dimensions() {
            let diff = self.get(i) - other.get(i);
            distance += diff.abs();
        }
        distance
    }

    fn check_index(&self, index: usize) {
        if index >= self.dimensions() {
            panic!("Cannot get index {} from {:?}", index, self.values);
        }
    }

    fn check_dimension(&self, other: &Self) {
        if self.dimensions() != other.dimensions() {
            panic!("Cannot get distance from {:?} to {:?}", self, other);
        }
    }
}
