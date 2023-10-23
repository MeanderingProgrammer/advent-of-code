use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::collections::HashSet;
use std::str::FromStr;

#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "U" => Ok(Self::Up),
            "D" => Ok(Self::Down),
            "L" => Ok(Self::Left),
            "R" => Ok(Self::Right),
            _ => Err("Unkown direction value".to_string()),
        }
    }
}

impl Direction {
    fn move_point(&self, p: &Point) -> Point {
        match self {
            Self::Up => p.add_y(1),
            Self::Down => p.add_y(-1),
            Self::Left => p.add_x(-1),
            Self::Right => p.add_x(1),
        }
    }
}

#[derive(Debug)]
struct Motion {
    direction: Direction,
    amount: i64,
}

impl FromStr for Motion {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (direction, amount) = s.split_once(" ").unwrap();
        Ok(Self {
            direction: direction.parse()?,
            amount: amount.parse().unwrap(),
        })
    }
}

fn main() {
    let motions = reader::read(|line| line.parse::<Motion>().unwrap());
    answer::part1(6563, follow_trail(&motions, 2));
    answer::part2(2653, follow_trail(&motions, 10));
}

fn follow_trail(motions: &Vec<Motion>, length: usize) -> usize {
    let mut rope = vec![Point::new(2); length];
    let mut tail_locations: HashSet<Point> = HashSet::new();

    motions.iter().for_each(|motion| {
        for _ in 0..motion.amount {
            rope[0] = motion.direction.move_point(&rope[0]);
            for i in 0..(rope.len() - 1) {
                rope[i + 1] = adjust_trail(&rope[i], &rope[i + 1]);
            }
            tail_locations.insert(rope.last().unwrap().clone());
        }
    });

    tail_locations.len()
}

fn adjust_trail(front: &Point, back: &Point) -> Point {
    if front.distance(back) < 2.0 {
        back.clone()
    } else {
        back.add_x(get_adjustment(back.x(), front.x()))
            .add_y(get_adjustment(back.y(), front.y()))
    }
}

fn get_adjustment(tail_val: i64, head_val: i64) -> i64 {
    match tail_val.cmp(&head_val) {
        std::cmp::Ordering::Less => 1,
        std::cmp::Ordering::Equal => 0,
        std::cmp::Ordering::Greater => -1,
    }
}
