use aoc_lib::answer;
use aoc_lib::reader;
use nom::{
    bytes::complete::{tag, take_till},
    character::complete::digit1,
    sequence::separated_pair,
    IResult,
};
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
            "turn on " => Ok(Self::TurnOn),
            "turn off " => Ok(Self::TurnOff),
            "toggle " => Ok(Self::Toggle),
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
    start: (usize, usize),
    end: (usize, usize),
}

impl Direction {
    fn from_str(input: &str) -> IResult<&str, Self> {
        fn parse_point(input: &str) -> IResult<&str, (usize, usize)> {
            // 660,55
            let (input, (x, y)) = separated_pair(digit1, tag(","), digit1)(input)?;
            Ok((input, (x.parse().unwrap(), y.parse().unwrap())))
        }
        // <action> <point> through <point>
        let (input, action) = take_till(|ch: char| ch.is_digit(10))(input)?;
        let (input, start) = parse_point(input)?;
        let (input, _) = tag(" through ")(input)?;
        let (input, end) = parse_point(input)?;
        Ok((
            input,
            Self {
                action: Action::from_str(action).unwrap(),
                start,
                end,
            },
        ))
    }

    fn apply(&self, grid: &mut Vec<i64>, f: fn(&Action, i64) -> i64) {
        for x in self.start.0..=self.end.0 {
            for y in self.start.1..=self.end.1 {
                let index = (x * 1_000) + y;
                grid[index] = f(&self.action, grid[index]);
            }
        }
    }
}

fn main() {
    let directions = reader::read(|line| Direction::from_str(line).unwrap().1);
    answer::part1(400410, apply_all(&directions, Action::single));
    answer::part2(15343601, apply_all(&directions, Action::dimable));
}

fn apply_all(directions: &Vec<Direction>, f: fn(&Action, i64) -> i64) -> i64 {
    let mut grid: Vec<i64> = vec![0; 1_000_000];
    directions
        .iter()
        .for_each(|direction| direction.apply(&mut grid, f));
    grid.into_iter().sum()
}
