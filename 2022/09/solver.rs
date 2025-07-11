use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Motion {
    direction: Direction,
    amount: i64,
}

impl FromStr for Motion {
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
    let motions = Reader::default().lines();
    answer::part1(6563, follow_trail(&motions, 2));
    answer::part2(2653, follow_trail(&motions, 10));
}

fn follow_trail(motions: &[Motion], length: usize) -> usize {
    let mut rope = vec![Point::default(); length];
    let mut tail_locations: HashSet<Point> = HashSet::default();

    motions.iter().for_each(|motion| {
        for _ in 0..motion.amount {
            rope[0] = rope[0].add(&motion.direction);
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
        back.add(Point::new(
            get_adjustment(back.x, front.x),
            get_adjustment(back.y, front.y),
        ))
    }
}

fn get_adjustment(tail_val: i32, head_val: i32) -> i32 {
    match tail_val.cmp(&head_val) {
        std::cmp::Ordering::Less => 1,
        std::cmp::Ordering::Equal => 0,
        std::cmp::Ordering::Greater => -1,
    }
}
