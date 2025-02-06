use aoc::{answer, Point, Reader, Str};
use std::str::FromStr;

#[derive(Debug)]
enum Action {
    TurnOn,
    TurnOff,
    Toggle,
}

impl FromStr for Action {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "on" => Ok(Self::TurnOn),
            "off" => Ok(Self::TurnOff),
            "toggle" => Ok(Self::Toggle),
            _ => Err(format!("Unknow action: {s}")),
        }
    }
}

impl Action {
    fn single(&self, current: i64) -> i64 {
        match self {
            Self::TurnOn => 1,
            Self::TurnOff => 0,
            Self::Toggle => 1 - current,
        }
    }

    fn dimable(&self, current: i64) -> i64 {
        match self {
            Self::TurnOn => current + 1,
            Self::TurnOff => 0.max(current - 1),
            Self::Toggle => current + 2,
        }
    }
}

#[derive(Debug)]
struct Direction {
    action: Action,
    start: Point,
    end: Point,
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // <action> <point> through <point>
        let [start, end] = [2, 0].map(|i| Str::nth_rev(s, ' ', i));
        Ok(Self {
            action: Str::nth_rev(s, ' ', 3),
            start,
            end,
        })
    }
}

impl Direction {
    fn apply(&self, grid: &mut [i64], f: fn(&Action, i64) -> i64) {
        for x in self.start.x..=self.end.x {
            for y in self.start.y..=self.end.y {
                let index = ((x * 1_000) + y) as usize;
                grid[index] = f(&self.action, grid[index]);
            }
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let directions = Reader::default().lines();
    answer::part1(400410, apply_all(&directions, Action::single));
    answer::part2(15343601, apply_all(&directions, Action::dimable));
}

fn apply_all(directions: &[Direction], f: fn(&Action, i64) -> i64) -> i64 {
    let mut grid: Vec<i64> = vec![0; 1_000_000];
    directions
        .iter()
        .for_each(|direction| direction.apply(&mut grid, f));
    grid.into_iter().sum()
}
