use aoc_lib::answer;
use aoc_lib::grid::{Bound, Grid};
use aoc_lib::point::Point;
use aoc_lib::reader;
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

struct Edge {
    bound: Bound,
    direction: Direction,
    next: fn(i64, i64, i64) -> Point,
}

impl Edge {
    fn new(start: Point, end: Point, direction: Direction, next: fn(i64, i64, i64) -> Point) -> Self {
        Self {
            bound: Bound::new(start, end),
            direction: direction,
            next: next,
        }
    }
}

struct Cube {
    grid: Grid<Space>,
    size: i64,
    edges: Vec<Edge>,
}

impl Cube {
    fn new(grid: Grid<Space>) -> Self {
        let total_spaces = grid.points().len();
        let spaces_per_face = total_spaces / 6;
        let size = (spaces_per_face as f64).sqrt() as i64;

        Self {
            grid,
            size,
            // Hard coding edge behavior :(
            edges: vec![
                Edge::new(
                    Point::new_2d(size, 0),
                    Point::new_2d(2 * size - 1, 0),
                    Direction::Right,
                    |x, _, size| Point::new_2d(0, 2 * size + x),
                ),
                Edge::new(
                    Point::new_2d(2 * size, 0),
                    Point::new_2d(3 * size - 1, 0),
                    Direction::Up,
                    |x, _, size| Point::new_2d(x - 2 * size, 4 * size - 1),
                ),
                Edge::new(
                    Point::new_2d(3 * size - 1, 0),
                    Point::new_2d(3 * size - 1, size - 1),
                    Direction::Left,
                    |_, y, size| Point::new_2d(2 * size - 1, 2 * size + (size - y - 1)),
                ),
                Edge::new(
                    Point::new_2d(2 * size, size - 1),
                    Point::new_2d(3 * size - 1, size -1),
                    Direction::Left,
                    |x, _, size| Point::new_2d(2 * size - 1, x - size),
                ),
                Edge::new(
                    Point::new_2d(2 * size -1, size),
                    Point::new_2d(2 * size - 1, 2 * size - 1),
                    Direction::Up,
                    |_, y, size| Point::new_2d(y + size, size - 1),
                ),
                Edge::new(
                    Point::new_2d(2 * size - 1, 2 * size),
                    Point::new_2d(2 * size - 1, 3 * size - 1),
                    Direction::Left,
                    |_, y, size| Point::new_2d(3 * size - 1, size - (y - 2 * size)),
                ),
                Edge::new(
                    Point::new_2d(size, 3 * size - 1),
                    Point::new_2d(2 * size - 1, 3 * size - 1),
                    Direction::Left,
                    |x, _, size| Point::new_2d(size - 1, x + 2 * size),
                ),
                Edge::new(
                    Point::new_2d(size - 1, 3 * size),
                    Point::new_2d(size - 1, 4 * size - 1),
                    Direction::Up,
                    |_, y, size| Point::new_2d(y - 2 * size, 3 * size - 1),
                ),
                Edge::new(
                    Point::new_2d(0, 4 * size - 1),
                    Point::new_2d(size - 1, 4 * size - 1),
                    Direction::Down,
                    |x, _, size| Point::new_2d(3 * size - 1 - x, 0),
                ),
                Edge::new(
                    Point::new_2d(0, 3 * size),
                    Point::new_2d(0, 4 * size - 1),
                    Direction::Down,
                    |_, y, size| Point::new_2d(y - 2 * size, 0),
                ),
                Edge::new(
                    Point::new_2d(0, 2 * size),
                    Point::new_2d(0, 3 * size - 1),
                    Direction::Right,
                    |_, y, size| Point::new_2d(size, 3 * size - 1 - y),
                ),
                Edge::new(
                    Point::new_2d(0, 2 * size),
                    Point::new_2d(size - 1, 2 * size),
                    Direction::Right,
                    |x, _, size| Point::new_2d(size, size + x),
                ),
                Edge::new(
                    Point::new_2d(size, size),
                    Point::new_2d(size, 2 * size - 1),
                    Direction::Down,
                    |_, y, size| Point::new_2d(y - size, 2 * size),
                ),
                Edge::new(
                    Point::new_2d(size, 0),
                    Point::new_2d(size, size - 1),
                    Direction::Right,
                    |_, y, size| Point::new_2d(0, 3 * size - 1 - y),
                ),
            ],
        }
    }

    fn next(&self, current: &mut State) {
        let next_position = current.next();
        if self.grid.contains(&next_position) {
            if self.legal(&next_position) {
                current.position = next_position;
            }
        } else {
            let edge = self.edges.iter()
                .find(|edge| edge.bound.contain(&current.position))
                .unwrap();
            let (x, y) = (current.position.x(), current.position.y());
            let cube_position = (edge.next)(x, y, self.size);
            //println!("{:?}", current.position);
            //println!("{:?}", cube_position);
            if self.legal(&cube_position) {
                current.position = cube_position;
                current.direction = edge.direction.clone();
            }
        }
    }

    fn legal(&self, position: &Point) -> bool {
        self.grid.get(position) != &Space::Wall
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

#[derive(Debug)]
struct State {
    position: Point,
    direction: Direction,
}

impl State {
    fn score(&self) -> i64 {
        let row_score = (self.position.y() + 1) * 1_000;
        let column_score = (self.position.x() + 1) * 4;
        let direction_score = match self.direction {
            Direction::Right => 0,
            Direction::Down => 1,
            Direction::Left => 2,
            Direction::Up => 3,
        };
        row_score + column_score + direction_score
    }
}

impl State {
    fn next(&self) -> Point {
        match self.direction {
            Direction::Up => self.position.add_y(-1),
            Direction::Right => self.position.add_x(1),
            Direction::Down => self.position.add_y(1),
            Direction::Left => self.position.add_x(-1),
        }
    }
}

fn main() {
    let (cube, instructions) = get_input();
    simulate(&cube, &instructions);
    //answer::part1(3590, simulate(false));
    // 15217 too low
    answer::part2(15217, simulate(&cube, &instructions));
}

fn simulate(cube: &Cube, instructions: &Vec<Instruction>) -> i64 {
    // This will differ for different inputs
    let mut state = State {
        position: Point::new_2d(cube.size, 0),
        direction: Direction::Right,
    };

    println!("{:?}", state);
    for instruction in instructions {
        //println!("{:?}", instruction);
        match instruction {
            Instruction::Move(amount) => {
                for _ in 0..*amount {
                    cube.next(&mut state);
                    //println!("{} - {:?}", i, state);
                }
            },
            Instruction::Turn(turn) => {
                state.direction = state.direction.turn(turn);
            },
        }
        //println!("{:?}", state);
    }

    state.score()
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
        .map(|part| {
            match part {
                "L" => Instruction::Turn(Turn::Left),
                "R" => Instruction::Turn(Turn::Right),
                amount => Instruction::Move(amount.parse::<i64>().unwrap()),
            }
        })
        .collect()
}
