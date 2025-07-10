use aoc::prelude::*;

#[derive(Debug, Eq, PartialEq, Hash)]
struct FuelCell {
    x: i32,
    y: i32,
}

impl FuelCell {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }

    fn add(&self, dx: i32, dy: i32) -> Self {
        Self::new(self.x + dx, self.y + dy)
    }

    fn power_level(&self, serial_number: i32) -> i32 {
        let rack_id = self.x + 10;
        let initial_power_level = rack_id * self.y;
        let power_level = (initial_power_level + serial_number) * rack_id;
        (power_level / 100) % 10 - 5
    }
}

#[derive(Debug)]
struct PowerGrid {
    size: i32,
    grid: HashMap<FuelCell, i32>,
}

impl PowerGrid {
    fn new(serial_number: i32, size: i32) -> Self {
        let mut grid = HashMap::default();
        for x in 1..=size {
            for y in 1..=size {
                let fuel_cell = FuelCell::new(x, y);
                let power_level = fuel_cell.power_level(serial_number);
                let above = grid.get(&fuel_cell.add(0, -1)).unwrap_or(&0);
                let left = grid.get(&fuel_cell.add(-1, 0)).unwrap_or(&0);
                let overlap = grid.get(&fuel_cell.add(-1, -1)).unwrap_or(&0);
                grid.insert(fuel_cell, above + left + power_level - overlap);
            }
        }
        Self { size, grid }
    }

    fn get_largest_size(&self) -> Point3d {
        let mut result = (0, 0, 0, 0);
        for sub_grid_size in 1..self.size {
            let largest = self.get_largest(sub_grid_size);
            if largest.2 > result.2 {
                result = (largest.0, largest.1, largest.2, sub_grid_size);
            }
        }
        Point3d::new(result.0, result.1, result.3)
    }

    fn get_largest(&self, size: i32) -> (i32, i32, i32) {
        let mut result = (0, 0, 0);
        for x in 1..=self.size - size {
            for y in 1..=self.size - size {
                let fuel_cell = FuelCell::new(x, y);
                let power = self.get_power(&fuel_cell, size);
                if power > result.2 {
                    result = (x, y, power);
                }
            }
        }
        result
    }

    fn get_power(&self, fuel_cell: &FuelCell, size: i32) -> i32 {
        let total = self.get(&fuel_cell.add(size - 1, size - 1));
        let above = self.get(&fuel_cell.add(size - 1, -1));
        let left = self.get(&fuel_cell.add(-1, size - 1));
        let overlap = self.get(&fuel_cell.add(-1, -1));
        total - above - left + overlap
    }

    fn get(&self, fuel_cell: &FuelCell) -> i32 {
        *self.grid.get(fuel_cell).unwrap_or(&0)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values = Reader::default().lines();
    let power_grid = PowerGrid::new(values[0], 300);
    let largest_3 = power_grid.get_largest(3);
    answer::part1(Point::new(243, 43), Point::new(largest_3.0, largest_3.1));
    answer::part2(Point3d::new(236, 151, 15), power_grid.get_largest_size());
}
