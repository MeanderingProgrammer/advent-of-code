use aoc::{answer, Point3d, Reader};
use std::str::FromStr;

#[derive(Debug)]
enum Direction {
    Forward,
    Down,
    Up,
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "forward" => Ok(Self::Forward),
            "down" => Ok(Self::Down),
            "up" => Ok(Self::Up),
            _ => Err(format!("Unknow direction: {s}")),
        }
    }
}

#[derive(Debug)]
struct Instruction {
    direction: Direction,
    amount: i32,
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (direction, amount) = s.split_once(' ').unwrap();
        Ok(Self {
            direction: direction.parse()?,
            amount: amount.parse().unwrap(),
        })
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions: Vec<Instruction> = Reader::default().read_from_str();

    let mut p = Point3d::default();
    instructions.iter().for_each(|instruction| {
        match instruction.direction {
            Direction::Forward => {
                // X (horizontal) works the same way in parts 1 & 2
                // Y is used for part 2 depth and unused by part 1
                p = p.add(Point3d::new(
                    instruction.amount,
                    p.z * instruction.amount,
                    0,
                ));
            }
            // Z functions as depth for part 1 & aim for part 2
            Direction::Down => p = p.add(Point3d::new(0, 0, instruction.amount)),
            Direction::Up => p = p.add(Point3d::new(0, 0, -instruction.amount)),
        }
    });

    answer::part1(1459206, p.x * p.z);
    answer::part2(1320534480, p.x * p.y);
}
