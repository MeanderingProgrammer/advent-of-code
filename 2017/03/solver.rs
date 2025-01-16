use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Context {
    grid: Grid<i64>,
    point: Point,
    value: i64,
    direction: Direction,
}

impl Default for Context {
    fn default() -> Self {
        let mut grid = Grid::default();
        let (point, value) = (Point::default(), 1);
        grid.add(point.clone(), value);
        Self {
            grid,
            point,
            value,
            direction: Direction::Right,
        }
    }
}

impl Context {
    fn next(&mut self, part1: bool) {
        self.point = &self.point + &self.direction;
        self.value = if part1 {
            self.value + 1
        } else {
            self.point
                .diagonal_neighbors()
                .into_iter()
                .map(|point| self.grid.get_or(&point).unwrap_or(&0))
                .sum()
        };
        self.grid.add(self.point.clone(), self.value);
        let next_direction = self.direction.left();
        if !self.grid.contains(&(&self.point + &next_direction)) {
            self.direction = next_direction;
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let goal = Reader::default().read_int()[0];
    answer::part1(419, compute(goal, true));
    answer::part2(295229, compute(goal, false));
}

fn compute(goal: i64, part1: bool) -> i64 {
    let mut context = Context::default();
    while context.value < goal {
        context.next(part1);
    }
    if part1 {
        context.point.length()
    } else {
        context.value
    }
}
