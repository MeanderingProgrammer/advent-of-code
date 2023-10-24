use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::line::Line2d;
use aoc_lib::point::Point;
use aoc_lib::reader;

#[derive(Debug)]
struct SandFlow {
    grid: Grid<char>,
    with_floor: bool,
    max_height: i64,
    start: Point,
}

impl SandFlow {
    fn new(grid: Grid<char>, with_floor: bool) -> Self {
        let bounds = grid.bounds(0);
        Self {
            grid,
            with_floor,
            max_height: bounds.upper().y() + if with_floor { 1 } else { 0 },
            start: Point::new_2d(500, 0),
        }
    }

    fn drop_grain(&mut self) -> bool {
        let mut grain = self.start.clone();
        while grain.y() < self.max_height {
            let next = vec![(0, 1), (-1, 1), (1, 1)]
                .into_iter()
                .map(|(x, y)| grain.add_x(x).add_y(y))
                .filter(|point| !self.grid.contains(&point))
                .next();
            if next.is_none() {
                break;
            }
            grain = next.unwrap();
        }
        if self.with_floor || grain.y() < self.max_height {
            self.grid.add(grain.clone(), 'O');
        }
        if self.with_floor {
            grain == self.start
        } else {
            grain.y() >= self.max_height
        }
    }

    fn amount_sand(&self) -> usize {
        self.grid.points_with_value('O').len()
    }
}

fn main() {
    answer::part1(610, fill(false));
    answer::part2(27194, fill(true));
}

fn fill(with_floor: bool) -> usize {
    let mut sand_flow = SandFlow::new(get_grid(), with_floor);
    let mut full = false;
    while !full {
        full |= sand_flow.drop_grain();
    }
    sand_flow.amount_sand()
}

fn get_grid() -> Grid<char> {
    let rock_formations: Vec<Vec<Point>> = reader::read(|line| {
        line.to_string()
            .split(" -> ")
            .map(|point| match point.split_once(",") {
                Some((x, y)) => Point::new_2d(x.parse().unwrap(), y.parse().unwrap()),
                None => panic!(),
            })
            .collect()
    });

    let mut grid: Grid<char> = Grid::new();
    rock_formations
        .iter()
        .flat_map(|rock_formation| {
            (1..rock_formation.len())
                .map(|i| Line2d::new(rock_formation[i - 1].clone(), rock_formation[i].clone()))
        })
        .flat_map(|line| line.as_points().into_iter())
        .for_each(|point| grid.add(point.clone(), '#'));
    grid
}
