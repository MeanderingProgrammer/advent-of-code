use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::reader;
use fxhash::FxHashSet;

type Point = (i16, i16);

#[derive(Debug)]
struct Garden {
    start: Point,
    walls: FxHashSet<Point>,
    len: i16,
}

impl Garden {
    fn new(grid: Grid<char>) -> Self {
        let starts = grid.points_with_value('S');
        Self {
            start: (starts[0].x as i16, starts[0].y as i16),
            walls: grid
                .points_with_value('#')
                .into_iter()
                .map(|point| (point.x as i16, point.y as i16))
                .collect(),
            len: (grid.bounds(0).upper.x as i16) + 1,
        }
    }

    fn step_n(&self, current: FxHashSet<Point>, n: i16) -> (i64, FxHashSet<Point>) {
        let mut result = current;
        for _ in 0..n {
            result = result
                .into_iter()
                .flat_map(|(x, y)| [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
                .filter(|point| !self.is_wall(point))
                .collect();
        }
        (result.len() as i64, result)
    }

    fn is_wall(&self, (x, y): &Point) -> bool {
        let (x, y) = (x.rem_euclid(self.len), y.rem_euclid(self.len));
        self.walls.contains(&(x, y))
    }
}

fn main() {
    let grid = reader::read_grid(|ch| Some(ch));
    let garden = Garden::new(grid);

    let mut points: FxHashSet<Point> = FxHashSet::default();
    points.insert(garden.start.clone());
    let (part1, points) = garden.step_n(points, 64);

    // Quadratic pattern in a growing diamond shape
    // https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7
    let (f0, points) = garden.step_n(points, 1);
    let (f1, points) = garden.step_n(points, garden.len);
    let (f2, _) = garden.step_n(points, garden.len);
    let n = (26501365 - 65) / (garden.len as i64);
    let part2 = solve_quadratic([f0, f1, f2], n);

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
