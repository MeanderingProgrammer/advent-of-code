use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
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

    fn x_value_at(&self, y: i64) -> i64 {
        (y - self.y_intercept) / self.slope
    }
}

#[derive(Debug, Clone, Ord, PartialOrd, Eq, PartialEq)]
struct Range {
    min: i64,
    max: i64,
}

impl Range {
    fn new(center: i64, offset: i64) -> Self {
        Self {
            min: center - offset,
            max: center + offset,
        }
    }

    fn contains(&self, value: i64) -> bool {
        value >= self.min && value <= self.max
    }

    fn can_join(&self, value: i64) -> bool {
        value >= self.min && value <= self.max + 1
    }

    fn len(&self) -> i64 {
        self.max - self.min
    }

    fn join(&self, other: &Self) -> Self {
        if !self.can_join(other.min) {
            panic!("No overlap, cannot join");
        }
        Self {
            min: self.min.min(other.min),
            max: self.max.max(other.max),
        }
    }
}

#[derive(Debug)]
struct CoverageZone {
    top_right: Line,
    top_left: Line,
    bottom_right: Line,
    bottom_left: Line,
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
                top_right: Line::new(-1, y + x + radius),
                top_left: Line::new(1, y - x + radius),
                bottom_right: Line::new(1, y - x - radius),
                bottom_left: Line::new(-1, y + x - radius),
                x_range: Range::new(x, radius),
                y_range: Range::new(y, radius),
            },
        ))
    }

    fn overlap_at_y(&self, y: i64) -> Option<Range> {
        if !self.y_range.contains(y) {
            return None;
        }
        let intercepts = vec![
            self.top_right.x_value_at(y),
            self.top_left.x_value_at(y),
            self.bottom_right.x_value_at(y),
            self.bottom_left.x_value_at(y),
        ];
        let valid_intercepts: Vec<i64> = intercepts
            .iter()
            .map(|&intercept| intercept)
            .filter(|&intercept| self.x_range.contains(intercept))
            .collect();

        match valid_intercepts.len() {
            0 => None,
            2 | 4 => Some(Range {
                min: *valid_intercepts.iter().min().unwrap(),
                max: *valid_intercepts.iter().max().unwrap(),
            }),
            _ => panic!("Should never be anyting other than 0, 2, or 4 intercepts"),
        }
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
    let mut overlaps: Vec<Range> = coverage
        .iter()
        .map(|zone| zone.overlap_at_y(y))
        .filter(|overlap| overlap.is_some())
        .map(|overlap| overlap.unwrap())
        .collect();
    overlaps.sort();

    let mut joined = overlaps[0].clone();
    for i in 1..overlaps.len() {
        let overlap = &overlaps[i];
        if joined.can_join(overlap.min) {
            joined = joined.join(overlap);
        } else {
            return joined;
        }
    }
    joined
}

fn tuning_frequency(coverage: &Vec<CoverageZone>, max_value: i64) -> i64 {
    for y in 0..=max_value {
        let covered = covered_range(coverage, y);
        if covered.max <= max_value {
            return ((covered.max + 1) * 4_000_000) + y;
        }
    }
    unreachable!()
}
