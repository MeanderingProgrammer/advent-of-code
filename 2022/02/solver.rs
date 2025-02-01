use aoc::{answer, Reader};
use std::str::FromStr;

#[derive(Debug, PartialEq)]
enum Hand {
    Rock,
    Paper,
    Scissors,
}

impl FromStr for Hand {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" | "X" => Ok(Self::Rock),
            "B" | "Y" => Ok(Self::Paper),
            "C" | "Z" => Ok(Self::Scissors),
            _ => Err("Unknown hand value".to_string()),
        }
    }
}

impl Hand {
    fn value(&self) -> i64 {
        match self {
            Hand::Rock => 1,
            Hand::Paper => 2,
            Hand::Scissors => 3,
        }
    }

    fn beats(&self) -> Self {
        match self {
            Self::Rock => Self::Scissors,
            Self::Paper => Self::Rock,
            Self::Scissors => Self::Paper,
        }
    }

    fn loses(&self) -> Self {
        match self {
            Self::Rock => Self::Paper,
            Self::Paper => Self::Scissors,
            Self::Scissors => Self::Rock,
        }
    }
}

#[derive(Debug)]
enum Outcome {
    Win,
    Lose,
    Draw,
}

impl FromStr for Outcome {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "X" => Ok(Self::Lose),
            "Y" => Ok(Self::Draw),
            "Z" => Ok(Self::Win),
            _ => Err("Unknown outcome value".to_string()),
        }
    }
}

impl Outcome {
    fn value(&self) -> i64 {
        match self {
            Self::Win => 6,
            Self::Lose => 0,
            Self::Draw => 3,
        }
    }
}

#[derive(Debug)]
struct Round {
    opponent_hand: Hand,
    hand: Hand,
    desired_outcome: Outcome,
}

impl FromStr for Round {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (opponent, me) = s.split_once(' ').unwrap();
        Ok(Self {
            opponent_hand: opponent.parse()?,
            hand: me.parse()?,
            desired_outcome: me.parse()?,
        })
    }
}

impl Round {
    fn score_play(&self) -> i64 {
        let outcome = if self.opponent_hand == self.hand {
            Outcome::Draw
        } else if self.opponent_hand.beats() == self.hand {
            Outcome::Lose
        } else {
            Outcome::Win
        };
        outcome.value() + self.hand.value()
    }

    fn score_result(&self) -> i64 {
        let hand_value = match self.desired_outcome {
            Outcome::Draw => self.opponent_hand.value(),
            Outcome::Lose => self.opponent_hand.beats().value(),
            Outcome::Win => self.opponent_hand.loses().value(),
        };
        hand_value + self.desired_outcome.value()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let rounds: Vec<Round> = Reader::default().read_from_str();
    answer::part1(9651, rounds.iter().map(|round| round.score_play()).sum());
    answer::part2(10560, rounds.iter().map(|round| round.score_result()).sum());
}
