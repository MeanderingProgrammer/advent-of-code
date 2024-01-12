use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
use itertools::Itertools;
use nom::{
    bytes::complete::tag,
    character::complete::digit0,
    combinator::{map_res, opt},
    sequence::tuple,
    IResult,
};

#[derive(Debug)]
struct Line {
    slope: i64,
    y_intercept: i64,
}

impl Line {
    fn new(slope: i64, y_intercept: i64) -> Self {
        Self { slope, y_intercept }
    }

    fn x(&self, y: i64) -> i64 {
        (y - self.y_intercept) / self.slope
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
    lines: Vec<Line>,
    x_range: Range,
    y_range: Range,
}

impl CoverageZone {
    fn from_str(input: &str) -> IResult<&str, Self> {
        fn parse_number(input: &str) -> IResult<&str, i64> {
            map_res(
                tuple((opt(tag("-")), digit0)),
                |(sign, s): (Option<&str>, &str)| (sign.unwrap_or("").to_string() + s).parse(),
            )(input)
        }

        fn parse_point(input: &str) -> IResult<&str, Point> {
            // x=2389280, y=2368338
            let (input, _) = tag("x=")(input)?;
            let (input, x) = parse_number(input)?;
            let (input, _) = tag(", y=")(input)?;
            let (input, y) = parse_number(input)?;
            Ok((input, Point::new(x, y)))
        }

        // Sensor at <point>: closest beacon is at <point>
        let (input, _) = tag("Sensor at ")(input)?;
        let (input, center) = parse_point(input)?;
        let (input, _) = tag(": closest beacon is at ")(input)?;
        let (input, beacon) = parse_point(input)?;

        let (x, y) = (center.x, center.y);
        let radius = center.manhattan_distance(&beacon);

        Ok((
            input,
            Self {
                lines: vec![
                    Line::new(-1, y + x + radius),
                    Line::new(1, y - x + radius),
                    Line::new(1, y - x - radius),
                    Line::new(-1, y + x - radius),
                ],
                x_range: Range::new(x - radius, x + radius),
                y_range: Range::new(y - radius, y + radius),
            },
        ))
    }

    fn overlap_at_y(&self, y: i64) -> Option<Range> {
        if !self.y_range.contains(y) {
            return None;
        }
        let valid_intercepts: Vec<i64> = self
            .lines
            .iter()
            .map(|line| line.x(y))
            .filter(|&intercept| self.x_range.contains(intercept))
            .collect();
        Some(Range::new(
            *valid_intercepts.iter().min().unwrap(),
            *valid_intercepts.iter().max().unwrap(),
        ))
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let coverage = reader::read(|line| CoverageZone::from_str(line).unwrap().1);
    answer::part1(5809294, covered_range(&coverage, 2_000_000).len());
    answer::part2(10693731308112, tuning_frequency(&coverage, 4_000_000));
}

fn covered_range(coverage: &Vec<CoverageZone>, y: i64) -> Range {
    let overlaps: Vec<Range> = coverage
        .iter()
        .flat_map(|zone| zone.overlap_at_y(y))
        .sorted()
        .collect();

    let mut joined = overlaps[0].clone();
    for i in 1..overlaps.len() {
        let overlap = &overlaps[i];
        if joined.contains(overlap.min) {
            joined.join(overlap);
        } else {
            return joined;
        }
    }
    joined
}

fn tuning_frequency(coverage: &Vec<CoverageZone>, max_value: i64) -> i64 {
    (0..=max_value)
        .into_iter()
        .map(|y| (covered_range(coverage, y).max + 1, y))
        .filter(|(x, _)| *x <= max_value)
        .next()
        .map(|(x, y)| (x * 4_000_000) + y)
        .unwrap()
}
