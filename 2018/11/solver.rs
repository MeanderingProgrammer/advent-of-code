use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq, Hash)]
struct FuelCell {
    x: i64,
    y: i64,
}

impl FuelCell {
    fn new(x: i64, y: i64) -> Self {
        Self { x, y }
    }

    fn add(&self, dx: i64, dy: i64) -> Self {
        Self::new(self.x + dx, self.y + dy)
    }

    fn power_level(&self, serial_number: i64) -> i64 {
        let rack_id = self.x + 10;
        let initial_power_level = rack_id * self.y;
        let power_level = (initial_power_level + serial_number) * rack_id;
        (power_level / 100) % 10 - 5
    }
}

#[derive(Debug)]
struct PowerGrid {
    size: i64,
    grid: HashMap<FuelCell, i64>,
}

impl PowerGrid {
    fn new(serial_number: i64, size: i64) -> Self {
        let mut grid = HashMap::new();
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

    fn get_largest_size(&self) -> (i64, i64, i64) {
        let mut result = (0, 0, 0, 0);
        for sub_grid_size in 1..self.size {
            let largest = self.get_largest(sub_grid_size);
            if largest.2 > result.2 {
                result = (largest.0, largest.1, largest.2, sub_grid_size);
            }
        }
        (result.0, result.1, result.3)
    }

    fn get_largest(&self, size: i64) -> (i64, i64, i64) {
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

    fn get_power(&self, fuel_cell: &FuelCell, size: i64) -> i64 {
        let total = self.get(&fuel_cell.add(size - 1, size - 1));
        let above = self.get(&fuel_cell.add(size - 1, -1));
        let left = self.get(&fuel_cell.add(-1, size - 1));
        let overlap = self.get(&fuel_cell.add(-1, -1));
        total - above - left + overlap
    }

    fn get(&self, fuel_cell: &FuelCell) -> i64 {
        *self.grid.get(fuel_cell).unwrap_or(&0)
    }
}

fn main() {
    let values = reader::read_int();
    let power_grid = PowerGrid::new(values[0], 300);
    let largest_3 = power_grid.get_largest(3);
    answer::part1((243, 43), (largest_3.0, largest_3.1));
    answer::part2((236, 151, 15), power_grid.get_largest_size());
}
