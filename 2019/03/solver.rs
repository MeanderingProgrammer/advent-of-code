use aoc_lib::answer;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::str::FromStr;

#[derive(Debug)]
struct Path {
    distances: FxHashMap<Point, i64>,
}

impl FromStr for Path {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut point = Point::default();
        let mut distance = 0;
        let mut distances = FxHashMap::default();
        s.split(",").for_each(|step| {
            let direction = Direction::from_str(&step[..1]).unwrap();
            let amount: usize = step[1..].parse().unwrap();
            (0..amount).for_each(|_| {
                point = &point + &direction;
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
    let paths = Reader::default().read(|line| Path::from_str(line).unwrap());
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

fn min_value<F>(points: &[Point], f: F) -> i64
where
    F: FnMut(&Point) -> i64,
{
    points.iter().map(f).min().unwrap()
}
