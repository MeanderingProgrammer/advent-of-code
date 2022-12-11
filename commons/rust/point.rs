#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Point {
    values: Vec<i64>,
}

impl Point {
    pub fn new(dimensions: usize) -> Point {
        Point {
            values: vec![0; dimensions],
        }
    }

    pub fn new_2d(x: i64, y: i64) -> Point {
        Point {
            values: vec![x, y],
        }
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

    pub fn add_y(&self, value: i64) -> Self  {
        self.add(1, value)
    }

    pub fn add_z(&self, value: i64) -> Self  {
        self.add(2, value)
    }

    fn add(&self, index: usize, value: i64) -> Self {
        self.check_index(index);
        let mut copied = self.values.clone();
        copied[index] += value;
        Point { values: copied }
    }

    pub fn distance(&self, other: &Self) -> f64 {
        if self.dimensions() != other.dimensions() {
            panic!("Cannot get distance from {:?} to {:?}", self, other);
        }
        let mut sum_squares = 0;
        for i in 0..self.dimensions() {
            let diff = self.get(i) - other.get(i);
            sum_squares += diff.pow(2);
        }
        (sum_squares as f64).sqrt()
    }

    fn check_index(&self, index: usize) {
        if index >= self.dimensions() {
            panic!("Cannot get index {} from {:?}", index, self.values);
        }
    }
}
