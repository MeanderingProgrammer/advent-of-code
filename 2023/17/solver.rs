use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Node {
    position: Point,
    directions: Vec<Direction>,
}

impl Node {
    fn get_neighbors(&self, length: usize) -> Vec<(Direction, bool, Vec<Point>)> {
        // Handle turning directions which must extend out to the specified length
        // Initially all directions are considered a turn, afterwards it is the
        // directions which are not straight or backwards
        let turns = match self.directions.first() {
            None => vec![
                Direction::Up,
                Direction::Down,
                Direction::Left,
                Direction::Right,
            ],
            Some(direction) => match direction {
                Direction::Up | Direction::Down => vec![Direction::Left, Direction::Right],
                Direction::Left | Direction::Right => vec![Direction::Up, Direction::Down],
            },
        };
        let mut neighbors: Vec<(Direction, bool, Vec<Point>)> = turns
            .into_iter()
            .map(|turn| {
                let positions = (1..=length)
                    .map(|i| &self.position + &(&turn.to_point() * (i as i64)))
                    .collect();
                (turn, true, positions)
            })
            .collect();
        // Add in the forward direction which does not need to extend to the length
        match self.directions.first() {
            None => (),
            Some(direction) => {
                let position = &self.position + direction;
                neighbors.push((direction.clone(), false, vec![position]));
            }
        };
        neighbors
    }
}

#[derive(Debug)]
struct Search<'a> {
    grid: &'a Grid<u32>,
    target: &'a Point,
    resistance: usize,
    max_repeats: usize,
}

impl<'a> Dijkstra for Search<'a> {
    type T = Node;

    fn done(&self, node: &Node) -> bool {
        &node.position == self.target
    }

    fn neighbors(&self, node: &Node) -> impl Iterator<Item = (Node, i64)> {
        node.get_neighbors(self.resistance)
            .into_iter()
            .filter(|(_, _, positions)| self.grid.contains(positions.last().unwrap()))
            .filter_map(|(direction, is_turn, positions)| {
                let mut directions = vec![direction.clone(); positions.len()];
                if !is_turn {
                    directions.append(&mut node.directions.clone());
                }
                if directions.len() <= self.max_repeats {
                    let next_node = Node {
                        position: positions.last().unwrap().clone(),
                        directions,
                    };
                    let cost = positions
                        .iter()
                        .map(|position| *self.grid.get(position) as i64)
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

fn min_heat(grid: &Grid<u32>, resistance: usize, max_repeats: usize) -> Option<i64> {
    let bounds = grid.bounds(0);
    let start = &Node {
        position: bounds.lower,
        directions: vec![],
    };
    let target = &bounds.upper;
    let search = Search {
        grid,
        target,
        resistance,
        max_repeats,
    };
    search.run(start)
}
