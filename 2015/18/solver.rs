use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashSet;

type Point = (i64, i64);

fn add(p1: &Point, p2: &Point) -> Point {
    (p1.0 + p2.0, p1.1 + p2.1)
}

#[derive(Debug)]
struct Animator {
    force_corners: bool,
    on: HashSet<Point>,
    min_x: i64,
    max_x: i64,
    min_y: i64,
    max_y: i64,
}

impl Animator {
    fn add_corners(&mut self) {
        if self.force_corners {
            self.on.insert((self.min_x, self.min_y));
            self.on.insert((self.min_x, self.max_y));
            self.on.insert((self.max_x, self.min_y));
            self.on.insert((self.max_x, self.max_y));
        }
    }

    fn step(&mut self) {
        let mut next_on = HashSet::new();
        for x in self.min_x..=self.max_x {
            for y in self.min_y..=self.max_y {
                let point = (x, y);
                let neighbors_on = self.neighbors_on(&point);
                let neighbors_needed = if self.on.contains(&point) {
                    vec![2, 3]
                } else {
                    vec![3]
                };
                if neighbors_needed.contains(&neighbors_on) {
                    next_on.insert(point);
                }
            }
        }
        self.on = next_on;
        self.add_corners();
    }

    fn neighbors_on(&self, point: &Point) -> usize {
        let directions = vec![
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ];
        directions
            .iter()
            .filter(|direction| self.on.contains(&add(point, direction)))
            .count()
    }

    fn lights_on(&self) -> usize {
        self.on.len()
    }
}

fn main() {
    let lines = reader::read_lines();
    answer::part1(1061, run(&lines, false));
    answer::part2(1006, run(&lines, true));
}

fn run(lines: &Vec<String>, force_corners: bool) -> usize {
    let mut on = HashSet::new();
    let mut min_x = 0;
    let mut max_x = 0;
    let mut min_y = 0;
    let mut max_y = 0;
    for (y, line) in lines.iter().enumerate() {
        min_y = min_y.min(y);
        max_y = max_y.max(y);
        for (x, value) in line.chars().enumerate() {
            min_x = min_x.min(x);
            max_x = max_x.max(x);
            if value == '#' {
                on.insert((x as i64, y as i64));
            }
        }
    }
    let mut animator = Animator {
        force_corners,
        on,
        min_x: min_x as i64,
        max_x: max_x as i64,
        min_y: min_y as i64,
        max_y: max_y as i64,
    };
    animator.add_corners();
    for _ in 0..100 {
        animator.step();
    }
    animator.lights_on()
}
