use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use itertools::{Itertools, MinMaxResult};
use std::str::FromStr;

#[derive(Debug)]
struct Line {
    m: i64,
    b: i64,
}

impl Line {
    fn new(m: i64, b: i64) -> Self {
        Self { m, b }
    }

    fn x(&self, y: i64) -> i64 {
        (y - self.b) / self.m
    }
}

#[derive(Debug, Clone, Ord, PartialOrd, Eq, PartialEq)]
struct Range {
    min: i64,
    max: i64,
}

impl Range {
    fn new(min: i64, max: i64) -> Self {
        Self { min, max }
    }

    fn contains(&self, value: i64) -> bool {
        value >= self.min && value <= self.max
    }

    fn len(&self) -> i64 {
        self.max - self.min
    }

    fn join(&mut self, other: &Self) {
        self.max = self.max.max(other.max);
    }
}

#[derive(Debug)]
struct CoverageZone {
    lines: [Line; 4],
    xs: Range,
    ys: Range,
}

impl FromStr for CoverageZone {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        fn parse_point(s: &str) -> Point {
            // at x=2389280, y=2368338
            let (_, point) = s.split_once("at ").unwrap();
            let (x, y) = point.split_once(", ").unwrap();
            let (_, x) = x.split_once('=').unwrap();
            let (_, y) = y.split_once('=').unwrap();
            Point::new(x.parse().unwrap(), y.parse().unwrap())
        }

        // Sensor <point>: closest beacon is <point>
        let (sensor, beacon) = s.split_once(": ").unwrap();
        let center = parse_point(sensor);
        let beacon = parse_point(beacon);

        let (x, y) = (center.x, center.y);
        let radius = center.manhattan_distance(&beacon);

        Ok(Self {
            lines: [
                Line::new(1, y - x + radius),
                Line::new(1, y - x - radius),
                Line::new(-1, y + x + radius),
                Line::new(-1, y + x - radius),
            ],
            xs: Range::new(x - radius, x + radius),
            ys: Range::new(y - radius, y + radius),
        })
    }
}

impl CoverageZone {
    fn overlap(&self, y: i64) -> Option<Range> {
        if !self.ys.contains(y) {
            return None;
        }
        let intercepts = self
            .lines
            .iter()
            .map(|line| line.x(y))
            .filter(|&intercept| self.xs.contains(intercept))
            .minmax();
        match intercepts {
            MinMaxResult::MinMax(min, max) => Some(Range::new(min, max)),
            _ => None,
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let coverage = Reader::default().read_from_str();
    answer::part1(5809294, covered_range(&coverage, 2_000_000).len());
    answer::part2(10693731308112, tuning_frequency(&coverage, 4_000_000));
}

fn covered_range(coverage: &[CoverageZone], y: i64) -> Range {
    let overlaps: Vec<Range> = coverage
        .iter()
        .flat_map(|zone| zone.overlap(y))
        .sorted()
        .collect();
    let mut joined = overlaps[0].clone();
    overlaps.iter().skip(1).for_each(|overlap| {
        if joined.contains(overlap.min) {
            joined.join(overlap);
        }
    });
    joined
}

fn tuning_frequency(coverage: &[CoverageZone], max_value: i64) -> i64 {
    (0..=max_value)
        .map(|y| (covered_range(coverage, y).max + 1, y))
        .find(|(x, _)| *x <= max_value)
        .map(|(x, y)| (x * 4_000_000) + y)
        .unwrap()
}
