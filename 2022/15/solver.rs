use aoc::{answer, Iter, Point, Reader, Str};
use rayon::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Line {
    m: i32,
    b: i32,
}

impl Line {
    fn new(m: i32, b: i32) -> Self {
        Self { m, b }
    }

    fn x(&self, y: i32) -> i32 {
        (y - self.b) / self.m
    }
}

#[derive(Debug, Clone, Ord, PartialOrd, Eq, PartialEq)]
struct Range {
    min: i32,
    max: i32,
}

impl Range {
    fn new(min: i32, max: i32) -> Self {
        Self { min, max }
    }

    fn contains(&self, value: i32) -> bool {
        value >= self.min && value <= self.max
    }

    fn len(&self) -> i32 {
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
        // Sensor <point>: closest beacon is <point>
        let [center, beacon]: [Point; 2] = [0, 1].map(|i| Str::nth(s, ':', i));
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
    fn overlap(&self, y: i32) -> Option<Range> {
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
            Some((min, max)) => Some(Range::new(min, max)),
            _ => None,
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let coverage = Reader::default().lines();
    answer::part1(5809294, covered_range(&coverage, 2_000_000).len());
    answer::part2(10693731308112, tuning_frequency(&coverage, 4_000_000));
}

fn covered_range(coverage: &[CoverageZone], y: i32) -> Range {
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

fn tuning_frequency(coverage: &[CoverageZone], max_value: i32) -> i64 {
    (0..=max_value)
        .into_par_iter()
        .map(|y| (covered_range(coverage, y).max + 1, y))
        .find_any(|(x, _)| *x <= max_value)
        .map(|(x, y)| (x as i64 * 4_000_000) + y as i64)
        .unwrap()
}
