use aoc::{Direction, Grid, Point, Reader, answer};

#[derive(Debug)]
struct Context {
    grid: Grid<i32>,
    point: Point,
    value: i32,
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
        self.point = self.point.add(&self.direction);
        self.value = if part1 {
            self.value + 1
        } else {
            self.point
                .diagonal_neighbors()
                .into_iter()
                .map(|point| self.grid.get_or(&point, 0))
                .sum()
        };
        self.grid.add(self.point.clone(), self.value);
        let next_direction = self.direction.left();
        if !self.grid.has(&self.point.add(&next_direction)) {
            self.direction = next_direction;
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let goal = Reader::default().line();
    answer::part1(419, compute(goal, true));
    answer::part2(295229, compute(goal, false));
}

fn compute(goal: i32, part1: bool) -> i32 {
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
