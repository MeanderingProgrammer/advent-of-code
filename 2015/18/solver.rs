use aoc::prelude::*;

#[derive(Debug)]
struct Animator {
    force_corners: bool,
    on: HashSet<Point>,
    min: Point,
    max: Point,
}

impl Animator {
    fn add_corners(&mut self) {
        if self.force_corners {
            self.on.insert(self.min.clone());
            self.on.insert(Point::new(self.min.x, self.max.y));
            self.on.insert(Point::new(self.max.x, self.min.y));
            self.on.insert(self.max.clone());
        }
    }

    fn step(&mut self) {
        let mut next_on = HashSet::default();
        for x in self.min.x..=self.max.x {
            for y in self.min.y..=self.max.y {
                let point = Point::new(x, y);
                let neighbors_on = self.neighbors_on(&point);
                let neighbors_needed = if self.on.contains(&point) {
                    vec![2, 3]
                } else {
                    vec![3]
                };
                if neighbors_needed.contains(&neighbors_on) {
                    next_on.insert(point);
                }
            }
        }
        self.on = next_on;
        self.add_corners();
    }

    fn neighbors_on(&self, point: &Point) -> usize {
        point
            .all_neighbors()
            .iter()
            .filter(|point| self.on.contains(point))
            .count()
    }

    fn lights_on(&self) -> usize {
        self.on.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    answer::part1(1061, run(&grid, false));
    answer::part2(1006, run(&grid, true));
}

fn run(grid: &Grid<char>, force_corners: bool) -> usize {
    let bound = grid.bounds();
    let mut animator = Animator {
        force_corners,
        on: grid.values(&'#').into_iter().collect(),
        min: bound.lower.clone(),
        max: bound.upper.clone(),
    };
    animator.add_corners();
    for _ in 0..100 {
        animator.step();
    }
    animator.lights_on()
}
