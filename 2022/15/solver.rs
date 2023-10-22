use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;

#[derive(Debug)]
struct Line {
    slope: i64,
    y_intercept: i64,
}

impl Line {
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
    fn new(center: Point, radius: i64) -> Self {
        CoverageZone {
            top_right: Line {
                slope: -1,
                y_intercept: center.y() + center.x() + radius,
            },
            top_left: Line {
                slope: 1,
                y_intercept: center.y() - center.x() + radius,
            },
            bottom_right: Line {
                slope: 1,
                y_intercept: center.y() - center.x() - radius,
            },
            bottom_left: Line {
                slope: -1,
                y_intercept: center.y() + center.x() - radius,
            },
            x_range: Range {
                min: center.x() - radius,
                max: center.x() + radius,
            },
            y_range: Range {
                min: center.y() - radius,
                max: center.y() + radius,
            },
        }
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
    let coverage = get_coverage();
    answer::part1(5809294, get_covered_range(&coverage, 2_000_000).len());
    answer::part2(
        10693731308112,
        get_tuning_frequency(&coverage, 4_000_000).unwrap(),
    );
}

fn get_covered_range(coverage: &Vec<CoverageZone>, y: i64) -> Range {
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

fn get_tuning_frequency(coverage: &Vec<CoverageZone>, max_value: i64) -> Option<i64> {
    for y in 0..=max_value {
        let covered = get_covered_range(coverage, y);
        if covered.max <= max_value {
            return Some(((covered.max + 1) * 4_000_000) + y);
        }
    }
    None
}

fn get_coverage() -> Vec<CoverageZone> {
    reader::read(|line| {
        let (sensor_comp, beacon_comp) = line.split_once(": ").unwrap();
        let sensor = parse_point(sensor_comp);
        let radius = sensor.manhattan_distance(&parse_point(beacon_comp));
        CoverageZone::new(sensor, radius)
    })
}

fn parse_point(component: &str) -> Point {
    let point = component.split_once(" at ").unwrap().1;
    let (x, y) = point.split_once(", ").unwrap();
    Point::new_2d(parse_coord(x), parse_coord(y))
}

fn parse_coord(coord: &str) -> i64 {
    coord.split_once("=").unwrap().1.parse::<i64>().unwrap()
}
