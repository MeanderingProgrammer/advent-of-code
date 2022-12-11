use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::collections::HashSet;

fn main() {
    let lines = reader::read_lines();
    answer::part1(6563, follow_trail(lines.as_slice(), 2));
    answer::part2(2653, follow_trail(lines.as_slice(), 10));
}

fn follow_trail(lines: &[String], length: usize) -> usize {
    let mut rope = vec![Point::new(2); length];
    let mut tail_locations: HashSet<Point> = HashSet::new();

    lines.iter().for_each(|line| {
        let (direction, amount) = line.split_once(" ").unwrap();
        let n = amount.parse::<i64>().unwrap();
        for _ in 0..n {
            rope[0] = match direction {
                "R" => rope[0].add_x(1),
                "L" => rope[0].add_x(-1),
                "U" => rope[0].add_y(1),
                "D" => rope[0].add_y(-1),
                _ => unreachable!(),
            };
            for i in 0..(rope.len()-1) {
                rope[i+1] = adjust_trail(&rope[i], &rope[i+1]);
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
        back
            .add_x(get_adjustment(back.x(), front.x()))
            .add_y(get_adjustment(back.y(), front.y()))
    }
}

fn get_adjustment(tail_val: i64, head_val: i64) -> i64 {
    if tail_val < head_val {
        1
    } else if tail_val == head_val {
        0
    } else {
        -1
    }
}
