use aoc_lib::answer;
use aoc_lib::point::Point3d;
use aoc_lib::reader::Reader;

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
            amount: amount.parse().unwrap(),
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions = Reader::default().read(|line| Instruction::from_str(line));

    let mut p = Point3d::default();
    instructions.iter().for_each(|instruction| {
        match instruction.direction {
            Direction::Forward => {
                // X (horizontal) works the same way in parts 1 & 2
                // Y is used for part 2 depth and unused by part 1
                p = &p + &Point3d::new(instruction.amount, p.z * instruction.amount, 0);
            }
            // Z functions as depth for part 1 & aim for part 2
            Direction::Down => p = &p + &Point3d::new(0, 0, instruction.amount),
            Direction::Up => p = &p + &Point3d::new(0, 0, -instruction.amount),
        }
    });

    answer::part1(1459206, p.x * p.z);
    answer::part2(1320534480, p.x * p.y);
}
