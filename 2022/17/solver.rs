use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug, Clone)]
struct Shape {
    locations: Vec<Point>,
}

impl Shape {
    fn new(locations: Vec<Point>) -> Self {
        Shape { locations }
    }
}

#[derive(Debug)]
struct FallingShape {
    anchor: Point,
    shape: Shape,
}

impl FallingShape {
    fn new(shape: Shape, height: i64) -> Self {
        let anchor = Point::new(2, height + 4);
        FallingShape { anchor, shape }
    }

    fn points(&self) -> Vec<Point> {
        self.shape
            .locations
            .iter()
            .map(|point| point.add(self.anchor.x, self.anchor.y))
            .collect()
    }

    fn apply_jet(&self, jet: &char) -> Self {
        match jet {
            '<' => self.go(&Direction::Left),
            '>' => self.go(&Direction::Right),
            _ => panic!("Unhandled jet value"),
        }
    }

    fn go(&self, direction: &Direction) -> Self {
        Self {
            anchor: self.anchor.step(direction),
            shape: self.shape.clone(),
        }
    }

    fn collides(&self, grid: &Grid<char>) -> bool {
        self.points()
            .iter()
            .any(|point| grid.contains(&point) || point.y < 0 || point.x < 0 || point.x > 6)
    }
}

fn main() {
    let jets = reader::read_chars();

    let shapes = vec![
        // ####
        Shape::new(vec![
            Point::new(0, 0),
            Point::new(1, 0),
            Point::new(2, 0),
            Point::new(3, 0),
        ]),
        // .#.
        // ###
        // .#.
        Shape::new(vec![
            Point::new(1, 0),
            Point::new(0, 1),
            Point::new(1, 1),
            Point::new(2, 1),
            Point::new(1, 2),
        ]),
        // ..#
        // ..#
        // ###
        Shape::new(vec![
            Point::new(0, 0),
            Point::new(1, 0),
            Point::new(2, 0),
            Point::new(2, 1),
            Point::new(2, 2),
        ]),
        // #
        // #
        // #
        // #
        Shape::new(vec![
            Point::new(0, 0),
            Point::new(0, 1),
            Point::new(0, 2),
            Point::new(0, 3),
        ]),
        // ##
        // ##
        Shape::new(vec![
            Point::new(0, 0),
            Point::new(1, 0),
            Point::new(0, 1),
            Point::new(1, 1),
        ]),
    ];

    answer::part1(
        3209,
        simulate(2_022, jets.iter().cycle(), shapes.iter().cycle()),
    );
    answer::part2(
        1580758017509,
        simulate(
            1_000_000_000_000,
            jets.iter().cycle(),
            shapes.iter().cycle(),
        ),
    );
}

fn simulate<'a>(
    rocks_to_drop: i64,
    mut jets: impl Iterator<Item = &'a char>,
    mut shapes: impl Iterator<Item = &'a Shape>,
) -> i64 {
    let mut grid: Grid<char> = Grid::new();
    let mut cache: HashMap<String, (i64, i64)> = HashMap::new();

    let mut additional_height = 0;
    let mut rocks_dropped = 0;

    while rocks_dropped < rocks_to_drop {
        let height = grid.height().unwrap_or(-1);
        let shape = shapes.next().unwrap();

        let mut crashed = false;
        let mut falling_shape = FallingShape::new(shape.clone(), height);

        while !crashed {
            let next_position = falling_shape.apply_jet(jets.next().unwrap());
            falling_shape = if next_position.collides(&grid) {
                falling_shape
            } else {
                next_position
            };

            let next_position = falling_shape.go(&Direction::Up);
            falling_shape = if next_position.collides(&grid) {
                crashed = true;
                falling_shape
            } else {
                next_position
            };
        }

        falling_shape
            .points()
            .into_iter()
            .for_each(|point| grid.add(point, '#'));

        rocks_dropped += 1;

        let height = grid.height().unwrap() + 1;

        let value = grid.as_string(".", 0);
        if cache.contains_key(&value) {
            let (cache_rocks, cache_height) = cache.get(&value).unwrap();
            let (period_length, period_height) =
                (rocks_dropped - cache_rocks, height - cache_height);
            let periods_left = (rocks_to_drop - rocks_dropped) / period_length;

            // Once we have a cache hit we advance as many full periods as possible
            rocks_dropped += periods_left * period_length;
            additional_height += periods_left * period_height;
        } else {
            cache.insert(value, (rocks_dropped, height));
        }

        // Remove points that are far enough down that they'll never be touched by new rocks
        remove_points_below(&mut grid, height - 50);
    }

    grid.height().unwrap() + 1 + additional_height
}

fn remove_points_below(grid: &mut Grid<char>, threshold: i64) {
    let points_to_remove: Vec<Point> = grid
        .points()
        .iter()
        .filter(|point| point.y < threshold)
        .map(|&point| point.clone())
        .collect();

    for point in points_to_remove {
        grid.remove(&point);
    }
}
