use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Heading, Point};
use aoc_lib::reader::Reader;

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
            max_height: bounds.upper.y + if with_floor { 1 } else { 0 },
            start: Point::new(500, 0),
        }
    }

    fn drop_grain(&mut self) -> bool {
        let mut grain = self.start.clone();
        while grain.y < self.max_height {
            let next = vec![Heading::South, Heading::SouthWest, Heading::SouthEast]
                .into_iter()
                .map(|heading| &grain + &heading)
                .filter(|point| !self.grid.contains(&point))
                .next();
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
        self.grid.points_with_value('O').len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
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
    let rock_formations: Vec<Vec<Point>> = Reader::default().read(|line| {
        line.to_string()
            .split(" -> ")
            .map(|point| match point.split_once(",") {
                Some((x, y)) => Point::new(x.parse().unwrap(), y.parse().unwrap()),
                None => panic!(),
            })
            .collect()
    });

    let mut grid: Grid<char> = Grid::new();
    rock_formations
        .iter()
        .flat_map(|rock_formation| {
            (1..rock_formation.len())
                .flat_map(|i| get_points(&rock_formation[i - 1], &rock_formation[i]))
        })
        .for_each(|point| grid.add(point, '#'));
    grid
}

fn get_points(p1: &Point, p2: &Point) -> Vec<Point> {
    let (x1, x2) = (p1.x, p2.x);
    let (y1, y2) = (p1.y, p2.y);
    (x1.min(x2)..=x1.max(x2))
        .flat_map(move |x| (y1.min(y2)..=y1.max(y2)).map(move |y| Point::new(x, y)))
        .collect()
}
