use aoc::{answer, Direction, Grid, Iter, Point, Reader};

#[derive(Debug)]
struct Traverser {
    grid: Grid<char>,
}

impl Traverser {
    fn new(grid: Grid<char>) -> Self {
        Self { grid }
    }

    fn traverse(&self) -> Vec<Point> {
        let mut position: Option<Point> = self
            .grid
            .iter()
            .find(|(point, _)| point.y == 0)
            .map(|(point, _)| point.clone());
        let mut direction = Direction::Down;
        let mut seen: Vec<Point> = Vec::default();
        while let Some(point) = position {
            seen.push(point.clone());
            let forward = point.add(&direction);
            let next = if self.grid.has(&forward) {
                Some((forward, direction.clone()))
            } else {
                Direction::values()
                    .iter()
                    .map(|direction| (point.add(direction), direction.clone()))
                    .find(|(point, _)| self.valid(&seen, point))
            };
            match next {
                Some((p, d)) => {
                    (position, direction) = (Some(p), d);
                }
                None => {
                    position = None;
                }
            }
        }
        seen
    }

    fn valid(&self, seen: &[Point], point: &Point) -> bool {
        self.grid.has(point) && !seen.contains(point)
    }

    fn letters(&self, seen: &[Point]) -> String {
        seen.iter()
            .map(|point| self.grid[point])
            .filter(|value| !['-', '|', '+'].contains(value))
            .join("")
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(|ch| if ch == ' ' { None } else { Some(ch) });
    let traverser = Traverser::new(grid);
    let seen = traverser.traverse();
    answer::part1("NDWHOYRUEA", &traverser.letters(&seen));
    answer::part2(17540, seen.len());
}
