use aoc::{HashMap, HashSet, Point3d, Reader, answer};
use rayon::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Join {
    offset: Point3d,
    rotation: usize,
}

impl Join {
    fn apply(&self, p: &Point3d) -> Point3d {
        rotate(p, self.rotation).add(self.offset.clone())
    }
}

#[derive(Debug)]
struct Scanner {
    positions: Vec<Point3d>,
    points: HashSet<Point3d>,
}

impl FromStr for Scanner {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let points = s
            .lines()
            .skip(1)
            .map(|line| Point3d::from_str(line).unwrap())
            .collect();
        Ok(Self {
            // Each scanner is assumed to be at the origin initially
            positions: vec![Point3d::default()],
            points,
        })
    }
}

impl Scanner {
    fn find_join(&self, other: &Scanner) -> Option<Join> {
        (0..24)
            .into_par_iter()
            .find_map_any(|rotation| self.attempt(other, rotation, 12))
    }

    fn attempt(&self, other: &Scanner, rotation: usize, overlap: usize) -> Option<Join> {
        let mut offsets: HashMap<Point3d, usize> = HashMap::default();
        for p1 in &self.points {
            for p2 in &other.points {
                let offset = p1.sub(rotate(p2, rotation));
                let counter = offsets.entry(offset.clone()).or_insert(0);
                *counter += 1;
                if *counter >= overlap {
                    return Some(Join { offset, rotation });
                }
            }
        }
        None
    }

    fn join(&mut self, other: Scanner, join: Join) {
        other
            .positions
            .iter()
            .for_each(|p| self.positions.push(join.apply(p)));
        other.points.iter().for_each(|p| {
            self.points.insert(join.apply(p));
        });
    }

    fn largest_distance(&self) -> i32 {
        let mut result: i32 = 0;
        for i in 0..self.positions.len() - 1 {
            for j in i + 1..self.positions.len() {
                let difference = self.positions[i].sub(self.positions[j].clone());
                result = result.max(difference.length());
            }
        }
        result
    }
}

fn rotate(p: &Point3d, index: usize) -> Point3d {
    let (x, y, z) = (p.x, p.y, p.z);
    let (tx, ty, tz) = match index {
        0 => (x, y, z),
        1 => (x, -y, -z),
        2 => (x, z, -y),
        3 => (x, -z, y),
        4 => (-x, y, -z),
        5 => (-x, -y, z),
        6 => (-x, z, y),
        7 => (-x, -z, -y),
        8 => (y, -x, z),
        9 => (y, x, -z),
        10 => (y, z, x),
        11 => (y, -z, -x),
        12 => (-y, x, z),
        13 => (-y, -x, -z),
        14 => (-y, z, -x),
        15 => (-y, -z, x),
        16 => (z, y, -x),
        17 => (z, -y, x),
        18 => (z, x, y),
        19 => (z, -x, -y),
        20 => (-z, y, x),
        21 => (-z, -y, -x),
        22 => (-z, x, -y),
        23 => (-z, -x, y),
        _ => unreachable!(),
    };
    Point3d::new(tx, ty, tz)
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let scanners = Reader::default().groups();
    let joined = join_scanners(scanners);
    answer::part1(512, joined.points.len());
    answer::part2(16802, joined.largest_distance());
}

fn join_scanners(mut scanners: Vec<Scanner>) -> Scanner {
    let mut joined = scanners.pop().unwrap();
    while !scanners.is_empty() {
        let (i, join) = next(&joined, &scanners).unwrap();
        let scanner = scanners.remove(i);
        joined.join(scanner, join);
    }
    joined
}

fn next(joined: &Scanner, scanners: &[Scanner]) -> Option<(usize, Join)> {
    for (i, scanner) in scanners.iter().enumerate() {
        if let Some(join) = joined.find_join(scanner) {
            return Some((i, join));
        }
    }
    None
}
