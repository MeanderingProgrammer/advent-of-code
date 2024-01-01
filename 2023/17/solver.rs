use aoc_lib::answer;
use aoc_lib::reader;
use priority_queue::DoublePriorityQueue;
use std::collections::{HashMap, HashSet};

type Point = (i16, i16);
type Grid = HashMap<Point, u16>;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    fn move_point(&self, start: &Point, amount: i16) -> Point {
        match self {
            Self::Up => (start.0, start.1 - amount),
            Self::Down => (start.0, start.1 + amount),
            Self::Left => (start.0 - amount, start.1),
            Self::Right => (start.0 + amount, start.1),
        }
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Node {
    position: Point,
    directions: Vec<Direction>,
}

impl Node {
    fn get_neighbors(&self, length: usize) -> Vec<(Direction, Vec<Point>)> {
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
        let mut neighbors: Vec<(Direction, Vec<Point>)> = turns
            .into_iter()
            .map(|turn| {
                let positions = (1..=length)
                    .into_iter()
                    .map(|i| turn.move_point(&self.position, i as i16))
                    .collect();
                (turn, positions)
            })
            .collect();
        // Add in the forward direction which does not need to extend to the length
        match self.directions.first() {
            None => (),
            Some(direction) => {
                let position = direction.move_point(&self.position, 1);
                neighbors.push((direction.clone(), vec![position]));
            }
        };
        neighbors
    }
}

#[derive(Debug)]
struct Search {
    grid: Grid,
    start: Point,
    target: Point,
}

impl Search {
    fn dijkstra(&self, turn_resistance: usize, allowed_repeats: usize) -> Option<u16> {
        let mut queue = DoublePriorityQueue::new();
        let start_node = Node {
            position: self.start,
            directions: vec![],
        };
        queue.push_decrease(start_node, 0 as u16);
        let mut seen = HashSet::new();
        while !queue.is_empty() {
            let (node, weight) = queue.pop_min().unwrap();
            if node.position == self.target {
                return Some(weight);
            }
            if seen.contains(&node) {
                continue;
            } else {
                seen.insert(node.clone());
            }
            node.get_neighbors(turn_resistance)
                .into_iter()
                .filter(|(_, positions)| self.grid.contains_key(positions.last().unwrap()))
                .for_each(|(direction, positions)| {
                    let mut directions = vec![direction.clone(); positions.len()];
                    directions.append(&mut node.directions.clone());
                    let directions = directions.into_iter().take(allowed_repeats + 1).collect();
                    let next_node = Node {
                        position: positions.last().unwrap().clone(),
                        directions,
                    };
                    let repeats = next_node
                        .directions
                        .iter()
                        .filter(|next_direction| next_direction == &&direction)
                        .count();
                    if repeats <= allowed_repeats && !seen.contains(&next_node) {
                        let heat: u16 = positions
                            .iter()
                            .map(|position| self.grid.get(position).unwrap())
                            .sum();
                        queue.push_decrease(next_node, weight + heat);
                    }
                });
        }
        None
    }
}

fn main() {
    let grid = reader::read_grid(|ch| ch.to_digit(10));
    let bounds = grid.bounds(0);
    let mut simple_grid: Grid = HashMap::new();
    grid.get_grid().into_iter().for_each(|(point, value)| {
        simple_grid.insert(from_aoc(&point), value as u16);
    });
    let search = Search {
        grid: simple_grid,
        start: from_aoc(bounds.lower()),
        target: from_aoc(bounds.upper()),
    };

    let part1 = search.dijkstra(1, 3);
    let part2 = search.dijkstra(4, 10);
    answer::part1(694, part1.unwrap());
    answer::part2(829, part2.unwrap());
}

fn from_aoc(point: &aoc_lib::point::Point) -> Point {
    (point.x() as i16, point.y() as i16)
}
