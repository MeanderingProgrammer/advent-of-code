use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug, Clone)]
struct Range {
    start: i64,
    end: i64,
}

impl FromStr for Range {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // x=-48..-32 | y=26..41 | z=-47..-37
        let (_, s) = s.split_once('=').unwrap();
        let (start, end) = s.split_once("..").unwrap();
        Ok(Self {
            start: start.parse().unwrap(),
            end: end.parse().unwrap(),
        })
    }
}

impl Range {
    fn overlap(&self, other: &Self) -> Option<Self> {
        let start = self.start.max(other.start);
        let end = self.end.min(other.end);
        if start <= end {
            Some(Self { start, end })
        } else {
            None
        }
    }

    fn length(&self) -> i64 {
        (self.end - self.start) + 1
    }
}

#[derive(Debug, Clone)]
struct Bound {
    xs: Range,
    ys: Range,
    zs: Range,
}

impl FromStr for Bound {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // x=<Range>,y=<Range>,z=<Range>
        let ranges = s.split(',').collect::<Vec<_>>();
        Ok(Self {
            xs: ranges[0].parse().unwrap(),
            ys: ranges[1].parse().unwrap(),
            zs: ranges[2].parse().unwrap(),
        })
    }
}

impl Bound {
    fn overlap(&self, other: &Self) -> Option<Self> {
        let xs = self.xs.overlap(&other.xs);
        let ys = self.ys.overlap(&other.ys);
        let zs = self.zs.overlap(&other.zs);
        match (xs, ys, zs) {
            (Some(xs), Some(ys), Some(zs)) => Some(Self { xs, ys, zs }),
            _ => None,
        }
    }

    fn area(&self) -> i64 {
        let length = self.xs.length();
        let width = self.ys.length();
        let height = self.zs.length();
        length * width * height
    }
}

#[derive(Debug, Clone)]
struct Step {
    count: i64,
    bound: Bound,
}

impl FromStr for Step {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // on <Bound> | off <Bound>
        let (state, bound) = s.split_once(' ').unwrap();
        let count = if state == "on" {
            Some(1)
        } else if state == "off" {
            Some(-1)
        } else {
            None
        };
        Ok(Self {
            count: count.unwrap(),
            bound: bound.parse()?,
        })
    }
}

impl Step {
    fn disabled_overlap(&self, other: &Self) -> Option<Self> {
        self.bound.overlap(&other.bound).map(|bound| Self {
            count: -self.count,
            bound,
        })
    }

    fn negate(&self) -> Self {
        Self {
            count: -self.count,
            bound: self.bound.clone(),
        }
    }

    fn area(&self) -> i64 {
        self.count * self.bound.area()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let steps = Reader::default().lines();
    let steps = final_steps(steps);
    answer::part1(561032, total(&initialization(&steps)));
    answer::part2(1322825263376414, total(&steps));
}

fn final_steps(steps: Vec<Step>) -> Vec<Step> {
    let mut result = vec![steps[0].clone()];
    for step in steps.into_iter().skip(1) {
        result.append(&mut disabled_overlaps(&result, &step));
        if step.count > 0 {
            result.push(step);
        }
    }
    result
}

fn disabled_overlaps(steps: &[Step], other: &Step) -> Vec<Step> {
    steps
        .iter()
        .flat_map(|step| step.disabled_overlap(other))
        .collect()
}

fn initialization(steps: &[Step]) -> Vec<Step> {
    let range = Range {
        start: -50,
        end: 50,
    };
    let limit = Bound {
        xs: range.clone(),
        ys: range.clone(),
        zs: range.clone(),
    };
    let step = Step {
        count: 0,
        bound: limit,
    };
    // Need the negative to handle the fact that this will track the
    // area disabled by our limited bound
    disabled_overlaps(steps, &step)
        .iter()
        .map(|step| step.negate())
        .collect()
}

fn total(steps: &[Step]) -> i64 {
    steps.iter().map(|step| step.area()).sum()
}
