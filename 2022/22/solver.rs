use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use nom::{
    bytes::complete::tag,
    character::complete::{alpha0, digit0},
    combinator::map_res,
    error::Error,
    multi::separated_list0,
    sequence::separated_pair,
};
use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
enum Space {
    Open,
    Wall,
}

impl fmt::Display for Space {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let result = match self {
            Self::Open => ".",
            Self::Wall => "#",
        };
        write!(f, "{}", result)
    }
}

#[derive(Debug, Clone)]
struct Edge {
    block: Block,
    rotations: usize,
}

impl Edge {
    fn new(block: Block, rotations: usize) -> Result<Self, String> {
        Ok(Edge { block, rotations })
    }
}

#[derive(Debug)]
struct Edges {
    above: Edge,
    right: Edge,
    below: Edge,
    left: Edge,
}

impl Edges {
    fn get_edge(&self, direction: &Direction) -> &Edge {
        match direction {
            Direction::Right => &self.right,
            Direction::Down => &self.below,
            Direction::Left => &self.left,
            Direction::Up => &self.above,
        }
    }
}

#[derive(Debug)]
struct Cube {
    grid: Grid<Space>,
    size: i64,
}

impl Cube {
    fn new(grid: Grid<Space>) -> Self {
        let total_spaces = grid.points().len();
        let spaces_per_face = total_spaces / 6;
        let size = (spaces_per_face as f64).sqrt() as i64;

        Self { grid, size }
    }

    fn next(&self, current: &mut State, edges: &HashMap<Block, Edges>) {
        let mut next_relative_position = current.next();
        if self.in_relative_bounds(&next_relative_position) {
            if self.legal(&current.block.absolute(self.size, &next_relative_position)) {
                current.relative = next_relative_position;
            }
        } else {
            next_relative_position = Point::new_2d(
                (next_relative_position.x() + self.size) % self.size,
                (next_relative_position.y() + self.size) % self.size,
            );
            let mut next_direction = current.direction.clone();

            let edge = edges.get(&current.block).unwrap().get_edge(&current.direction);
            for _ in 0..edge.rotations {
                next_relative_position = Point::new_2d(
                    self.size - next_relative_position.y() - 1,
                    next_relative_position.x(),
                );
                next_direction = next_direction.turn(&Turn::Right);
            }

            if self.legal(&edge.block.absolute(self.size, &next_relative_position)) {
                current.block = edge.block.clone();
                current.relative = next_relative_position;
                current.direction = next_direction;
            }
        }
    }

    fn in_relative_bounds(&self, position: &Point) -> bool {
        let (x, y) = (position.x(), position.y());
        x >= 0 && x < self.size && y >= 0 && y < self.size
    }

    fn legal(&self, position: &Point) -> bool {
        self.grid.get(position) == &Space::Open
    }
}

#[derive(Debug)]
enum Turn {
    Right,
    Left,
}

#[derive(Debug)]
enum Instruction {
    Move(i64),
    Turn(Turn),
}

#[derive(Debug, Clone)]
enum Direction {
    Right,
    Down,
    Left,
    Up,
}

impl Direction {
    fn turn(&self, turn: &Turn) -> Self {
        match (self, turn) {
            (Self::Up, Turn::Left) => Self::Left,
            (Self::Up, Turn::Right) => Self::Right,
            (Self::Right, Turn::Left) => Self::Up,
            (Self::Right, Turn::Right) => Self::Down,
            (Self::Down, Turn::Left) => Self::Right,
            (Self::Down, Turn::Right) => Self::Left,
            (Self::Left, Turn::Left) => Self::Down,
            (Self::Left, Turn::Right) => Self::Up,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum Block {
    A,
    B,
    C,
    D,
    E,
    F,
}

impl Block {
    fn from_str(block: &str) -> Result<Self, String> {
        match block {
            "A" => Ok(Self::A),
            "B" => Ok(Self::B),
            "C" => Ok(Self::C),
            "D" => Ok(Self::D),
            "E" => Ok(Self::E),
            "F" => Ok(Self::F),
            _ => Err("Cannot parse block".to_string()),
        }
    }

    fn top_left(&self, size: i64) -> Point {
        // This will differ for different inputs
        let (col, row) = match self {
            Self::A => (1, 0),
            Self::B => (2, 0),
            Self::C => (1, 1),
            Self::D => (0, 2),
            Self::E => (1, 2),
            Self::F => (0, 3),
        };
        Point::new_2d(col * size, row * size)
    }

    fn absolute(&self, size: i64, relative: &Point) -> Point {
        self.top_left(size)
            .add_x(relative.x())
            .add_y(relative.y())
    }
}

#[derive(Debug)]
struct State {
    block: Block,
    size: i64,
    relative: Point,
    direction: Direction,
}

impl State {
    fn new(cube: &Cube) -> Self {
        // This will differ for different inputs
        Self {
            block: Block::A,
            size: cube.size,
            relative: Point::new_2d(0, 0),
            direction: Direction::Right,
        }
    }

    fn next(&self) -> Point {
        match self.direction {
            Direction::Up => self.relative.add_y(-1),
            Direction::Right => self.relative.add_x(1),
            Direction::Down => self.relative.add_y(1),
            Direction::Left => self.relative.add_x(-1),
        }
    }

    fn score(&self) -> i64 {
        let position = self.block.absolute(self.size, &self.relative);
        let row_score = (position.y() + 1) * 1_000;
        let column_score = (position.x() + 1) * 4;
        let direction_score = match self.direction {
            Direction::Right => 0,
            Direction::Down => 1,
            Direction::Left => 2,
            Direction::Up => 3,
        };
        row_score + column_score + direction_score
    }
}

fn main() {
    let (cube, instructions) = get_input();
    answer::part1(3590, simulate(&cube, &instructions, parse_mappings(vec![
        // This will differ for different inputs
        "A -> E:0 B:0 C:0 B:0",
        "B -> B:0 A:0 B:0 A:0",
        "C -> A:0 C:0 E:0 C:0",
        "D -> F:0 E:0 F:0 E:0",
        "E -> C:0 D:0 A:0 D:0",
        "F -> D:0 F:0 D:0 F:0",
    ])));
    answer::part2(86382, simulate(&cube, &instructions, parse_mappings(vec![
        // This will differ for different inputs
        "A -> F:1 B:0 C:0 D:2",
        "B -> F:0 E:2 C:1 A:0",
        "C -> A:0 B:3 E:0 D:3",
        "D -> C:1 E:0 F:0 A:2",
        "E -> C:0 B:2 F:1 D:0",
        "F -> D:0 E:3 B:0 A:3",
    ])));
}

fn simulate(cube: &Cube, instructions: &Vec<Instruction>, edges: HashMap<Block, Edges>) -> i64 {
    let mut state = State::new(cube);
    for instruction in instructions {
        match instruction {
            Instruction::Move(amount) => {
                for _ in 0..*amount {
                    cube.next(&mut state, &edges);
                }
            },
            Instruction::Turn(turn) => {
                state.direction = state.direction.turn(turn);
            },
        }
    }
    state.score()
}

fn parse_mappings(edge_mappings: Vec<&str>) -> HashMap<Block, Edges> {
    let mut parser = separated_pair::<_, _, _, _, Error<_>, _, _, _>(
        map_res(alpha0, Block::from_str),
        tag(" -> "),
        separated_list0(
            tag(" "),
            map_res(
                separated_pair(
                    map_res(alpha0, Block::from_str),
                    tag(":"),
                    map_res(digit0, |s: &str| s.parse::<usize>()),
                ),
                |(block, rotations)| Edge::new(block, rotations),
            ),
        ),
    );

    let mut result = HashMap::new();
    edge_mappings.iter()
        .map(|edge_mapping| parser(edge_mapping).unwrap().1)
        .for_each(|(block, edges)| {
            result.insert(block, Edges {
                above: edges[0].clone(),
                right: edges[1].clone(),
                below: edges[2].clone(),
                left: edges[3].clone(),
            });
        });
    result
}

fn get_input() -> (Cube, Vec<Instruction>) {
    let data = reader::read_group_lines();
    (
        parse_cube(&data[0]),
        parse_instructions(&data[1][0]),
    )
}

fn parse_cube(lines: &Vec<String>) -> Cube {
    let grid = Grid::from_lines(lines.clone(), |ch| match ch {
        '.' => Some(Space::Open),
        '#' => Some(Space::Wall),
        _ => None,
    });
    Cube::new(grid)
}

fn parse_instructions(line: &str) -> Vec<Instruction> {
    line.replace("L", ",L,")
        .replace("R", ",R,")
        .split(",")
        .map(|part| match part {
            "L" => Instruction::Turn(Turn::Left),
            "R" => Instruction::Turn(Turn::Right),
            amount => Instruction::Move(amount.parse::<i64>().unwrap()),
        })
        .collect()
}
