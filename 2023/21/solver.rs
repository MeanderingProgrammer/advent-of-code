use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::collections::HashSet;

#[derive(Debug)]
struct Garden {
    start: Point,
    walls: HashSet<Point>,
    len: i64,
}

impl Garden {
    fn new(grid: Grid<char>) -> Self {
        let starts = grid.points_with_value('S');
        Self {
            start: starts[0].clone(),
            walls: grid
                .points_with_value('#')
                .into_iter()
                .map(|point| point.clone())
                .collect(),
            len: grid.bounds(0).upper.x + 1,
        }
    }

    fn not_wall(&self, point: &Point) -> bool {
        let (x, y) = (point.x.rem_euclid(self.len), point.y.rem_euclid(self.len));
        !self.walls.contains(&Point::new(x, y))
    }

    fn step_n(&self, current: HashSet<Point>, n: i64) -> (i64, HashSet<Point>) {
        let mut result = current;
        for _ in 0..n {
            result = result
                .into_iter()
                .flat_map(|point| {
                    let neighbors = point.neighbors();
                    neighbors.into_iter().filter(|point| self.not_wall(point))
                })
                .collect();
        }
        (result.len() as i64, result)
    }
}

fn main() {
    let grid = reader::read_grid(|ch| Some(ch));
    let garden = Garden::new(grid);

    let mut points: HashSet<Point> = HashSet::new();
    points.insert(garden.start.clone());
    let (part1, points) = garden.step_n(points, 64);

    // Honestly no clue, something about patterns in a growing diamond shape
    // https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7
    let (a0, points) = garden.step_n(points, 1);
    let (a1, points) = garden.step_n(points, garden.len);
    let (a2, _) = garden.step_n(points, garden.len);
    let iterations = 26501365 / garden.len;
    let part2 = part2_magic(a0, a1, a2, iterations);

    answer::part1(3847, part1);
    answer::part2(637537341306357, part2);
}

fn part2_magic(a0: i64, a1: i64, a2: i64, n: i64) -> i64 {
    let b0 = a0;
    let b1 = a1 - a0;
    let b2 = a2 - a1 - b1;
    b0 + (b1 * n) + (n * (n - 1) / 2 * b2)
}
