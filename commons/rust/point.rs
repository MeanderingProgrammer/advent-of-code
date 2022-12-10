#[derive(Debug, PartialEq, Eq, Hash)]
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

    pub fn x(&self) -> i64 {
        self.get(0)
    }

    pub fn add_x(&self, value: i64) -> Self {
        self.add(0, value)
    }

    pub fn y(&self) -> i64 {
        self.get(1)
    }

    pub fn add_y(&self, value: i64) -> Self  {
        self.add(1, value)
    }

    pub fn z(&self) -> i64 {
        self.get(2)
    }

    pub fn add_z(&self, value: i64) -> Self  {
        self.add(2, value)
    }

    fn check_index(&self, index: usize) {
        if index >= self.values.len() {
            panic!("Cannot get index {} from {:?}", index, self.values)
        }
    }

    fn get(&self, index: usize) -> i64 {
        self.check_index(index);
        self.values[index]
    }

    fn add(&self, index: usize, value: i64) -> Self {
        self.check_index(index);
        let mut copied = self.values.clone();
        copied[index] += value;
        Point { values: copied }
    }
}
