use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Heading, Point};
use aoc_lib::reader::Reader;
use std::str::FromStr;

#[derive(Debug)]
struct RockFormation {
    points: Vec<Point>,
}

impl FromStr for RockFormation {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            points: s
                .split(" -> ")
                .map(|point| point.parse().unwrap())
                .collect(),
        })
    }
}

impl RockFormation {
    fn fill(&self) -> Vec<Point> {
        (1..self.points.len())
            .flat_map(|i| self.before(i))
            .collect()
    }

    fn before(&self, i: usize) -> Vec<Point> {
        let (p1, p2) = (&self.points[i - 1], &self.points[i]);
        let (x1, x2) = (p1.x, p2.x);
        let (y1, y2) = (p1.y, p2.y);
        (x1.min(x2)..=x1.max(x2))
            .flat_map(move |x| (y1.min(y2)..=y1.max(y2)).map(move |y| Point::new(x, y)))
            .collect()
    }
}

#[derive(Debug)]
struct SandFlow {
    grid: Grid<char>,
    with_floor: bool,
    max_height: i64,
    start: Point,
}

impl SandFlow {
    fn new(grid: Grid<char>, with_floor: bool) -> Self {
        let bounds = grid.bounds();
        Self {
            grid,
            with_floor,
            max_height: bounds.upper.y + if with_floor { 1 } else { 0 },
            start: Point::new(500, 0),
        }
    }

    fn drop_grain(&mut self) -> bool {
        let mut grain = self.start.clone();
        while grain.y < self.max_height {
            let next = [Heading::South, Heading::SouthWest, Heading::SouthEast]
                .iter()
                .map(|heading| grain.add(heading))
                .find(|point| !self.grid.contains(point));
            if next.is_none() {
                break;
            }
            grain = next.unwrap();
        }
        if self.with_floor || grain.y < self.max_height {
            self.grid.add(grain.clone(), 'O');
        }
        if self.with_floor {
            grain == self.start
        } else {
            grain.y >= self.max_height
        }
    }

    fn amount_sand(&self) -> usize {
        self.grid.get_values('O').len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let rock_formations: Vec<RockFormation> = Reader::default().read_from_str();
    let mut grid: Grid<char> = Grid::default();
    rock_formations
        .iter()
        .flat_map(|rock_formation| rock_formation.fill())
        .for_each(|point| grid.add(point, '#'));

    answer::part1(610, fill(grid.clone(), false));
    answer::part2(27194, fill(grid.clone(), true));
}

fn fill(grid: Grid<char>, with_floor: bool) -> usize {
    let mut sand_flow = SandFlow::new(grid, with_floor);
    let mut full = false;
    while !full {
        full |= sand_flow.drop_grain();
    }
    sand_flow.amount_sand()
}
