use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Node {
    point: Point,
    direction: Option<Direction>,
    length: u8,
}

impl Node {
    fn new(point: Point, direction: Option<Direction>, length: u8) -> Self {
        Self {
            point,
            direction,
            length,
        }
    }

    fn get_neighbors(&self) -> [Option<Direction>; 3] {
        match &self.direction {
            // Initially all directions are considered a turn
            None => [Some(Direction::Down), Some(Direction::Right), None],
            Some(direction) => [
                Some(direction.left()),
                Some(direction.right()),
                Some(direction.clone()),
            ],
        }
    }

    fn go(&self, direction: &Direction, n: u8) -> Point {
        let point: Point = direction.into();
        self.point.add(point.mul(n))
    }
}

#[derive(Debug)]
struct Search {
    grid: Grid<u16>,
    target: Point,
    resistance: u8,
    max_repeats: u8,
}

impl Dijkstra for Search {
    type T = Node;
    type W = u16;

    fn done(&self, node: &Self::T) -> bool {
        node.point == self.target
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        node.get_neighbors()
            .into_iter()
            .flatten()
            .filter_map(|direction| {
                let turn = node.direction != Some(direction.clone());
                // Turns must be extended out to the resistance
                let traveled = if turn { self.resistance } else { 1 };
                let length = traveled + if turn { 0 } else { node.length };
                let point = node.go(&direction, traveled);
                if length <= self.max_repeats && self.grid.has(&point) {
                    let cost = (1..=traveled)
                        .map(|i| node.go(&direction, i))
                        .map(|point| self.grid[&point])
                        .sum();
                    Some((Node::new(point, Some(direction), length), cost))
                } else {
                    None
                }
            })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(|ch| Some(ch.to_digit(10).unwrap() as u16));
    answer::part1(694, min_heat(&grid, 1, 3));
    answer::part2(829, min_heat(&grid, 4, 10));
}

fn min_heat(grid: &Grid<u16>, resistance: u8, max_repeats: u8) -> u16 {
    let bounds = grid.bounds();
    let start = Node::new(bounds.lower, None, 0);
    let search = Search {
        grid: grid.clone(),
        target: bounds.upper,
        resistance,
        max_repeats,
    };
    search.run(start).unwrap()
}
