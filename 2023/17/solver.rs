use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Node {
    position: Point,
    direction: Option<Direction>,
    length: u8,
}

impl Node {
    fn get_neighbors(&self, length: u8) -> Vec<(Direction, bool, Vec<Point>)> {
        // Handle turning directions which must extend out to the specified length
        // Initially all directions are considered a turn, afterwards it is the
        // directions which are not straight or backwards
        let turns = match &self.direction {
            None => [Direction::Down, Direction::Right],
            Some(direction) => match direction {
                Direction::Up | Direction::Down => [Direction::Left, Direction::Right],
                Direction::Left | Direction::Right => [Direction::Up, Direction::Down],
            },
        };
        let mut neighbors: Vec<(Direction, bool, Vec<Point>)> = turns
            .into_iter()
            .map(|turn| {
                let positions = (1..=length)
                    .map(|i| {
                        let point: Point = (&turn).into();
                        self.position.add(point.mul(i as i64))
                    })
                    .collect();
                (turn, true, positions)
            })
            .collect();
        // Add in the forward direction which does not need to extend to the length
        match &self.direction {
            None => (),
            Some(direction) => {
                let position = self.position.add(direction);
                neighbors.push((direction.clone(), false, vec![position]));
            }
        };
        neighbors
    }
}

#[derive(Debug)]
struct Search {
    grid: Grid<u32>,
    target: Point,
    resistance: u8,
    max_repeats: u8,
}

impl Dijkstra for Search {
    type T = Node;

    fn done(&self, node: &Node) -> bool {
        node.position == self.target
    }

    fn neighbors(&self, node: &Node) -> impl Iterator<Item = (Node, i64)> {
        node.get_neighbors(self.resistance)
            .into_iter()
            .filter(|(_, _, positions)| self.grid.has(positions.last().unwrap()))
            .filter_map(|(direction, is_turn, positions)| {
                let mut length = positions.len() as u8;
                length += if is_turn { 0 } else { node.length };
                if length <= self.max_repeats {
                    let next_node = Node {
                        position: positions.last().unwrap().clone(),
                        direction: Some(direction),
                        length,
                    };
                    let cost = positions
                        .iter()
                        .map(|position| self.grid[position] as i64)
                        .sum();
                    Some((next_node, cost))
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
    let grid = Reader::default().read_grid(|ch| ch.to_digit(10));
    answer::part1(694, min_heat(&grid, 1, 3).unwrap());
    answer::part2(829, min_heat(&grid, 4, 10).unwrap());
}

fn min_heat(grid: &Grid<u32>, resistance: u8, max_repeats: u8) -> Option<i64> {
    let bounds = grid.bounds();
    let start = Node {
        position: bounds.lower,
        direction: None,
        length: 0,
    };
    let search = Search {
        grid: grid.clone(),
        target: bounds.upper,
        resistance,
        max_repeats,
    };
    search.run(start)
}
