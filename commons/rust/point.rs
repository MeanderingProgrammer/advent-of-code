#[derive(Debug)]
pub struct Point {
    values: Vec<i64>,
}

impl Point {
    pub fn new(dimensions: usize) -> Point {
        Point {
            values: vec![0; dimensions],
        }
    }

    pub fn x(&self) -> i64 {
        self.get(0)
    }

    pub fn add_x(&mut self, value: i64)  {
        self.add(0, value);
    }

    pub fn y(&self) -> i64 {
        self.get(1)
    }

    pub fn add_y(&mut self, value: i64)  {
        self.add(1, value);
    }

    pub fn z(&self) -> i64 {
        self.get(2)
    }

    pub fn add_z(&mut self, value: i64)  {
        self.add(2, value);
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

    fn add(&mut self, index: usize, value: i64) {
        self.check_index(index);
        self.values[index] += value;
    }
}
