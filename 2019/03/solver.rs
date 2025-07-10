use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Path {
    distances: HashMap<Point, i32>,
}

impl FromStr for Path {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut point = Point::default();
        let mut distance = 0;
        let mut distances = HashMap::default();
        s.split(",").for_each(|step| {
            let direction = Direction::from_str(&step[..1]).unwrap();
            let amount: usize = step[1..].parse().unwrap();
            (0..amount).for_each(|_| {
                point = point.add(&direction);
                distance += 1;
                distances.entry(point.clone()).or_insert(distance);
            });
        });
        Ok(Self { distances })
    }
}

impl Path {
    fn intersection(&self, other: &Self) -> Vec<Point> {
        self.distances
            .keys()
            .filter(|point| other.distances.contains_key(point))
            .cloned()
            .collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let paths = Reader::default().lines::<Path>();
    let (p1, p2) = (&paths[0], &paths[1]);
    let intersection = p1.intersection(p2);
    answer::part1(870, min_value(&intersection, |point| point.length()));
    answer::part2(
        13698,
        min_value(&intersection, |point| {
            p1.distances[point] + p2.distances[point]
        }),
    );
}

fn min_value(points: &[Point], f: impl FnMut(&Point) -> i32) -> i32 {
    points.iter().map(f).min().unwrap()
}
