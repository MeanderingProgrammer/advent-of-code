use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;

#[derive(Debug)]
enum Direction {
    Forward,
    Down,
    Up,
}

impl Direction {
    fn from_str(direction: &str) -> Option<Self> {
        match direction {
            "forward" => Some(Self::Forward),
            "down" => Some(Self::Down),
            "up" => Some(Self::Up),
            _ => None,
        }
    }
}

#[derive(Debug)]
struct Instruction {
    direction: Direction,
    amount: i64,
}

impl Instruction {
    fn from_str(line: &str) -> Self {
        let (direction, amount) = line.split_once(" ").unwrap();
        Instruction {
            direction: Direction::from_str(direction).unwrap(),
            amount: amount.parse::<i64>().unwrap(),
        }
    }
}

fn main() {
    let instructions = reader::read(|line| Instruction::from_str(line));

    let mut p = Point::new(3);
    instructions.iter().for_each(|instruction| {
        match instruction.direction {
            Direction::Forward => {
                // X (horizontal) works the same way in parts 1 & 2
                p = p.add_x(instruction.amount);
                // Y is used for part 2 depth and unused by part 1
                p = p.add_y(p.z() * instruction.amount);
            }
            // Z functions as depth for part 1 & aim for part 2
            Direction::Down => p = p.add_z(instruction.amount),
            Direction::Up => p = p.add_z(-1 * instruction.amount),
        }
    });

    answer::part1(1459206, p.x() * p.z());
    answer::part2(1320534480, p.x() * p.y());
}
