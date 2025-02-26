use aoc::{HashSet, Iter, Point, Reader, answer};
use std::collections::VecDeque;

#[derive(Debug)]
struct Knot {
    lengths: Vec<usize>,
    q: VecDeque<usize>,
    skip_size: usize,
    skipped: Vec<usize>,
}

impl Knot {
    fn new(lengths: Vec<usize>) -> Self {
        Self {
            lengths,
            q: (0..256).collect(),
            skip_size: 0,
            skipped: Vec::default(),
        }
    }

    fn run_hash(&mut self) -> String {
        (0..64).for_each(|_| self.run());
        let skipped: usize = self.skipped.iter().sum();
        self.q.rotate_right(skipped % self.q.len());
        self.dense_hash()
            .chars()
            .map(|ch| u32::from_str_radix(&ch.to_string(), 16).unwrap())
            .map(|hex_bytes| format!("{:04b}", hex_bytes))
            .join("")
    }

    fn run(&mut self) {
        for length in self.lengths.iter() {
            let temp: Vec<usize> = self.q.drain(0..*length).collect();
            temp.iter().rev().for_each(|&value| self.q.push_back(value));
            self.q.rotate_left(self.skip_size % self.q.len());
            self.skipped.push(length + self.skip_size);
            self.skip_size += 1;
        }
    }

    fn dense_hash(&self) -> String {
        self.q
            .iter()
            .collect::<Vec<&usize>>()
            .chunks(16)
            .map(|chunk| {
                let mut hashed = 0;
                for value in chunk {
                    hashed ^= *value;
                }
                format!("{hashed:02x}")
            })
            .join("")
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let prefix = Reader::default().line();
    let points = enabled_points(prefix);
    answer::part1(8190, points.len());
    answer::part2(1134, group_points(points));
}

fn enabled_points(prefix: String) -> Vec<Point> {
    (0..128)
        .flat_map(|y| {
            let lengths = format!("{}-{}", prefix, y)
                .chars()
                .map(|ch| ch as usize)
                .chain([17, 31, 73, 47, 23])
                .collect();
            let mut knot = Knot::new(lengths);
            let hashed = knot.run_hash();
            hashed
                .char_indices()
                .filter(|&(_, value)| value == '1')
                .map(|(x, _)| Point::new(x as i32, y))
                .collect::<Vec<Point>>()
        })
        .collect()
}

fn group_points(points: Vec<Point>) -> usize {
    let mut groups: Vec<HashSet<Point>> = Vec::default();
    for point in points.into_iter() {
        let adjacent: HashSet<Point> = point.neighbors().into_iter().collect();
        let mut new_group: HashSet<Point> = [point].into_iter().collect();
        groups.retain(|group| match adjacent.is_disjoint(group) {
            true => true,
            false => {
                new_group.extend(group.clone());
                false
            }
        });
        groups.push(new_group);
    }
    groups.len()
}
