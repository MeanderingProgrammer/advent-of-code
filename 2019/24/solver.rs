use aoc_lib::answer;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct Location {
    point: Point,
    depth: i64,
}

impl Location {
    fn new(point: Point, depth: i64) -> Self {
        Self { point, depth }
    }
}

#[derive(Debug)]
struct Layout {
    grid: FxHashSet<Location>,
    recursive: bool,
    size: i32,
    middle: Point,
}

impl Layout {
    fn new(grid: FxHashSet<Location>, recursive: bool) -> Self {
        Self {
            grid,
            recursive,
            size: 5,
            middle: Point::new(2, 2),
        }
    }

    fn step(&mut self) {
        let mut counts: FxHashMap<Location, usize> = FxHashMap::default();
        self.grid
            .iter()
            .flat_map(|location| self.neighbors(location))
            .filter(|neighbor| self.valid(&neighbor.point))
            .for_each(|neighbor| *counts.entry(neighbor).or_default() += 1);

        self.grid = counts
            .into_iter()
            .filter(|(location, count)| {
                *count == 1 || (*count == 2 && !self.grid.contains(location))
            })
            .map(|(location, _)| location)
            .collect();
    }

    fn neighbors<'a>(&'a self, location: &'a Location) -> impl Iterator<Item = Location> + 'a {
        Direction::values().iter().flat_map(|direction| {
            let neighbor = location.point.add(direction);
            if self.recursive && neighbor == self.middle {
                (0..self.size)
                    .map(|i| match direction {
                        Direction::Up => Point::new(i, self.size - 1),
                        Direction::Down => Point::new(i, 0),
                        Direction::Left => Point::new(self.size - 1, i),
                        Direction::Right => Point::new(0, i),
                    })
                    .map(|p| Location::new(p, location.depth - 1))
                    .collect()
            } else if self.recursive && !self.valid(&neighbor) {
                vec![Location::new(
                    self.middle.add(direction),
                    location.depth + 1,
                )]
            } else {
                vec![Location::new(neighbor, location.depth)]
            }
        })
    }

    fn valid(&self, p: &Point) -> bool {
        p.x >= 0 && p.x < self.size && p.y >= 0 && p.y < self.size
    }

    fn diversity(&self) -> usize {
        self.grid
            .iter()
            .map(|location| &location.point)
            .map(|p| 2usize.pow((p.y as u32) * 5 + (p.x as u32)))
            .sum()
    }

    fn bugs(&self) -> usize {
        self.grid.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    let locations: FxHashSet<Location> = grid
        .values(&'#')
        .into_iter()
        .map(|point| Location::new(point, 0))
        .collect();
    answer::part1(32776479, part1(locations.clone()));
    answer::part2(2017, part2(locations.clone()));
}

fn part1(grid: FxHashSet<Location>) -> usize {
    let mut layout = Layout::new(grid, false);
    let mut seen = Vec::default();
    while !seen.contains(&layout.grid) {
        seen.push(layout.grid.clone());
        layout.step();
    }
    layout.diversity()
}

fn part2(grid: FxHashSet<Location>) -> usize {
    let mut layout = Layout::new(grid, true);
    for _ in 0..200 {
        layout.step();
    }
    layout.bugs()
}
