use aoc::prelude::*;

#[derive(Debug)]
struct Department {
    grid: HashSet<Point>,
}

impl Department {
    fn new(grid: &Grid<char>) -> Self {
        let grid = HashSet::from_iter(grid.values(&'@'));
        Self { grid }
    }

    fn cleanup(&mut self) -> Vec<usize> {
        let mut result = Vec::default();
        while let points = self.accessible()
            && !points.is_empty()
        {
            result.push(points.len());
            for point in points {
                self.grid.remove(&point);
            }
        }
        result
    }

    fn accessible(&self) -> Vec<Point> {
        self.grid
            .iter()
            .filter(|point| {
                let neighbors = point.all_neighbors();
                self.count(neighbors.into_iter()) < 4
            })
            .cloned()
            .collect()
    }

    fn count(&self, points: impl Iterator<Item = Point>) -> usize {
        points.filter(|point| self.grid.contains(point)).count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid::<char>();
    let mut department = Department::new(&grid);
    let removed = department.cleanup();
    answer::part1(1464, removed[0]);
    answer::part2(8409, removed.iter().sum());
}
