use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::str::FromStr;
use strum_macros::EnumString;

#[derive(Debug, EnumString)]
#[strum(ascii_case_insensitive)]
enum Direction {
    Forward,
    Down,
    Up,
}

#[derive(Debug)]
struct Instruction {
    direction: Direction,
    amount: i64,
}

fn main() {
    let instructions = reader::read(|line| {
        let (direction, amount) = line.split_once(" ").unwrap();
        Instruction {
            direction: Direction::from_str(direction).unwrap(),
            amount: amount.parse::<i64>().unwrap(),
        }
    });

    let mut p = Point::new(3);
    instructions.iter().for_each(|instruction| {
        match instruction.direction {
            Direction::Forward => {
                // X (horizontal) works the same way in parts 1 & 2
                p.add_x(instruction.amount);
                // Y is used for part 2 depth and unused by part 1
                p.add_y(p.z() * instruction.amount);
            },
            // Z functions as depth for part 1 & aim for part 2
            Direction::Down => p.add_z(instruction.amount),
            Direction::Up => p.add_z(-1 * instruction.amount),
        }
    });

    answer::part1(1459206, p.x() * p.z());
    answer::part2(1320534480, p.x() * p.y());
}
