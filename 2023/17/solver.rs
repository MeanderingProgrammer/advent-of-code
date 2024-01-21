use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::Search;

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
                    .into_iter()
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
struct Searcher {
    grid: Grid<u32>,
    start: Point,
    target: Point,
}

impl Searcher {
    fn min_heat(&self, turn_resistance: usize, allowed_repeats: usize) -> Option<i64> {
        Search {
            start: Node {
                position: self.start.clone(),
                directions: vec![],
            },
            is_done: |node| node.position == self.target,
            get_neighbors: |node| {
                node.get_neighbors(turn_resistance)
                    .into_iter()
                    .filter(|(_, _, positions)| self.grid.contains(positions.last().unwrap()))
                    .filter_map(|(direction, is_turn, positions)| {
                        let mut directions = vec![direction.clone(); positions.len()];
                        if !is_turn {
                            directions.append(&mut node.directions.clone());
                        }
                        let next_node = Node {
                            position: positions.last().unwrap().clone(),
                            directions,
                        };
                        let repeats = next_node.directions.len();
                        if repeats <= allowed_repeats {
                            let cost = positions
                                .iter()
                                .map(|position| *self.grid.get(position) as i64)
                                .sum();
                            Some((next_node, cost))
                        } else {
                            None
                        }
                    })
                    .collect()
            },
        }
        .dijkstra()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(|ch| ch.to_digit(10));
    let bounds = grid.bounds(0);
    let searcher = Searcher {
        grid,
        start: bounds.lower,
        target: bounds.upper,
    };
    let part1 = searcher.min_heat(1, 3);
    let part2 = searcher.min_heat(4, 10);
    answer::part1(694, part1.unwrap());
    answer::part2(829, part2.unwrap());
}
