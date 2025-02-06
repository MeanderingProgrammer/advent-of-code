use aoc::{answer, Grid, HashSet, Point, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
struct Garden {
    start: Point,
    walls: HashSet<Point>,
    len: i32,
}

impl Garden {
    fn new(grid: Grid<char>) -> Self {
        Self {
            start: grid.value(&'S'),
            walls: grid.values(&'#').into_iter().collect(),
            len: grid.bounds().upper.x + 1,
        }
    }

    fn step(&self, n: i32) -> i64 {
        let mut result: HashSet<Point> = HashSet::default();
        let mut seen: HashSet<Point> = HashSet::default();
        let mut q: VecDeque<(Point, i32)> = [(self.start.clone(), n)].into();
        while !q.is_empty() {
            let (point, steps) = q.pop_front().unwrap();
            // Any position reached with an even number of steps
            // remaining will remain reachable
            if steps % 2 == 0 {
                result.insert(point.clone());
            }
            if steps > 0 {
                for neighbor in point.neighbors() {
                    if !self.is_wall(&neighbor) && !seen.contains(&neighbor) {
                        seen.insert(neighbor.clone());
                        q.push_back((neighbor, steps - 1));
                    }
                }
            }
        }
        result.len() as i64
    }

    fn is_wall(&self, point: &Point) -> bool {
        let (x, y) = (point.x.rem_euclid(self.len), point.y.rem_euclid(self.len));
        self.walls.contains(&Point::new(x, y))
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    let garden = Garden::new(grid);

    let part1 = garden.step(64);

    // Quadratic pattern in a growing diamond shape
    // https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7
    let part2 = solve_quadratic(
        [
            garden.step(65),
            garden.step(65 + garden.len),
            garden.step(65 + 2 * garden.len),
        ],
        (26501365 - 65) / garden.len as i64,
    );

    answer::part1(3847, part1);
    answer::part2(637537341306357, part2);
}

fn solve_quadratic(f: [i64; 3], n: i64) -> i64 {
    // f(x) = ax² + bx + c = plots in 65 + 131 * x
    // Solving for c is easy since we have f[0]
    // f[0] = a(0)² + b(0) + c -> c = f[0]
    // Solve for b in terms of a using f[1] & c = f[0]
    // f[1] = a(1)² + b(1) + f[0]
    // b = f[1] - f[0] - a
    // Solve for a using f[2], b, & c = f[0]
    // f[2] = a(2)² + b(2) + f[0]
    // 4a + 2b = f[2] - f[0]
    // 4a + 2(f[1] - f[0] - a) = f[2] - f[0]
    // 4a + 2f[1] - 2f[0] - 2a = f[2] - f[0]
    // a = (f[2] - 2f[1] + f[0]) / 2
    let a = (f[2] - (2 * f[1]) + f[0]) / 2;
    let b = f[1] - f[0] - a;
    let c = f[0];
    a * n * n + b * n + c
}
