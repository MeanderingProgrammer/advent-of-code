use aoc::{answer, Direction, FromChar, Grid, HashMap, Point, Reader, Str};
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq)]
enum Space {
    Open,
    Wall,
}

impl FromChar for Space {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Open),
            '#' => Some(Self::Wall),
            _ => None,
        }
    }
}

#[derive(Debug, Clone)]
struct Edge {
    block: Block,
    rotations: usize,
}

impl FromStr for Edge {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (block, rotations) = s.split_once(':').unwrap();
        Ok(Self {
            block: block.parse()?,
            rotations: rotations.parse().unwrap(),
        })
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
    size: i32,
}

impl Cube {
    fn new(s: &str) -> Self {
        let grid: Grid<Space> = s.into();
        let total_spaces = grid.iter().count();
        let spaces_per_face = total_spaces / 6;
        let size = (spaces_per_face as f64).sqrt() as i32;
        Self { grid, size }
    }

    fn next(&self, current: &mut State, edges: &HashMap<Block, Edges>) {
        let mut next_relative_position = current.next();
        if self.in_relative_bounds(&next_relative_position) {
            if self.legal(&current.block.absolute(self.size, &next_relative_position)) {
                current.relative = next_relative_position;
            }
        } else {
            next_relative_position = Point::new(
                (next_relative_position.x + self.size) % self.size,
                (next_relative_position.y + self.size) % self.size,
            );
            let mut next_direction = current.direction.clone();

            let edge = edges
                .get(&current.block)
                .unwrap()
                .get_edge(&current.direction);
            for _ in 0..edge.rotations {
                next_relative_position = Point::new(
                    self.size - next_relative_position.y - 1,
                    next_relative_position.x,
                );
                next_direction = Turn::Right.turn(&next_direction);
            }

            if self.legal(&edge.block.absolute(self.size, &next_relative_position)) {
                current.block = edge.block.clone();
                current.relative = next_relative_position;
                current.direction = next_direction;
            }
        }
    }

    fn in_relative_bounds(&self, position: &Point) -> bool {
        let (x, y) = (position.x, position.y);
        x >= 0 && x < self.size && y >= 0 && y < self.size
    }

    fn legal(&self, position: &Point) -> bool {
        self.grid[position] == Space::Open
    }
}

#[derive(Debug)]
enum Turn {
    Right,
    Left,
}

impl Turn {
    fn turn(&self, direction: &Direction) -> Direction {
        match (direction, self) {
            (Direction::Up, Self::Left) | (Direction::Down, Self::Right) => Direction::Left,
            (Direction::Up, Self::Right) | (Direction::Down, Self::Left) => Direction::Right,
            (Direction::Right, Self::Left) | (Direction::Left, Self::Right) => Direction::Up,
            (Direction::Right, Self::Right) | (Direction::Left, Self::Left) => Direction::Down,
        }
    }
}

#[derive(Debug)]
enum Instruction {
    Move(usize),
    Turn(Turn),
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "L" => Ok(Self::Turn(Turn::Left)),
            "R" => Ok(Self::Turn(Turn::Right)),
            amount => Ok(Self::Move(amount.parse().unwrap())),
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

impl FromStr for Block {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" => Ok(Self::A),
            "B" => Ok(Self::B),
            "C" => Ok(Self::C),
            "D" => Ok(Self::D),
            "E" => Ok(Self::E),
            "F" => Ok(Self::F),
            _ => Err("Cannot parse block".to_string()),
        }
    }
}

impl Block {
    fn top_left(&self, size: i32) -> Point {
        // This will differ for different inputs
        let (col, row) = match self {
            Self::A => (1, 0),
            Self::B => (2, 0),
            Self::C => (1, 1),
            Self::D => (0, 2),
            Self::E => (1, 2),
            Self::F => (0, 3),
        };
        Point::new(col * size, row * size)
    }

    fn absolute(&self, size: i32, relative: &Point) -> Point {
        self.top_left(size).add(relative.clone())
    }
}

#[derive(Debug)]
struct State {
    block: Block,
    size: i32,
    relative: Point,
    direction: Direction,
}

impl State {
    fn new(cube: &Cube) -> Self {
        // This will differ for different inputs
        Self {
            block: Block::A,
            size: cube.size,
            relative: Point::default(),
            direction: Direction::Right,
        }
    }

    fn next(&self) -> Point {
        self.relative.add(&self.direction)
    }

    fn score(&self) -> i32 {
        let position = self.block.absolute(self.size, &self.relative);
        let row_score = (position.y + 1) * 1_000;
        let column_score = (position.x + 1) * 4;
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
    answer::timer(solution);
}

fn solution() {
    let data = Reader::default().groups::<String>();
    let cube = Cube::new(&data[0]);
    let instructions = parse_instructions(&data[1]);
    answer::part1(
        3590,
        simulate(
            &cube,
            &instructions,
            parse_mappings(&[
                // This will differ for different inputs
                "A -> E:0 B:0 C:0 B:0",
                "B -> B:0 A:0 B:0 A:0",
                "C -> A:0 C:0 E:0 C:0",
                "D -> F:0 E:0 F:0 E:0",
                "E -> C:0 D:0 A:0 D:0",
                "F -> D:0 F:0 D:0 F:0",
            ]),
        ),
    );
    answer::part2(
        86382,
        simulate(
            &cube,
            &instructions,
            parse_mappings(&[
                // This will differ for different inputs
                "A -> F:1 B:0 C:0 D:2",
                "B -> F:0 E:2 C:1 A:0",
                "C -> A:0 B:3 E:0 D:3",
                "D -> C:1 E:0 F:0 A:2",
                "E -> C:0 B:2 F:1 D:0",
                "F -> D:0 E:3 B:0 A:3",
            ]),
        ),
    );
}

fn parse_instructions(s: &str) -> Vec<Instruction> {
    s.replace('L', ",L,")
        .replace('R', ",R,")
        .split(',')
        .map(|part| part.parse().unwrap())
        .collect()
}

fn simulate(cube: &Cube, instructions: &[Instruction], edges: HashMap<Block, Edges>) -> i32 {
    let mut state = State::new(cube);
    for instruction in instructions {
        match instruction {
            Instruction::Move(amount) => {
                for _ in 0..*amount {
                    cube.next(&mut state, &edges);
                }
            }
            Instruction::Turn(turn) => {
                state.direction = turn.turn(&state.direction);
            }
        }
    }
    state.score()
}

fn parse_mappings(edge_mappings: &[&str]) -> HashMap<Block, Edges> {
    edge_mappings
        .iter()
        .map(|edge_mapping| parse_edge_mapping(edge_mapping))
        .collect()
}

fn parse_edge_mapping(s: &str) -> (Block, Edges) {
    // A -> F:1 B:0 C:0 D:2
    let (block, s) = s.split_once(" -> ").unwrap();
    let [above, right, below, left] = [0, 1, 2, 3].map(|i| Str::nth(s, ' ', i));
    (
        block.parse().unwrap(),
        Edges {
            above,
            right,
            below,
            left,
        },
    )
}
