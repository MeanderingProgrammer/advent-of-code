use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Clone, Debug, PartialEq)]
enum Hand {
    Rock,
    Paper,
    Scissors,
}

impl Hand {
    fn value(&self) -> i64 {
        return match self {
            Hand::Rock => 1,
            Hand::Paper => 2,
            Hand::Scissors => 3,
        }
    }

    fn beats(&self) -> Hand {
        return match self {
            Hand::Rock => Hand::Scissors,
            Hand::Paper => Hand::Rock,
            Hand::Scissors => Hand::Paper,
        }
    }

    fn loses(&self) -> Hand {
        return match self {
            Hand::Rock => Hand::Paper,
            Hand::Paper => Hand::Scissors,
            Hand::Scissors => Hand::Rock,
        }
    }
}

#[derive(Debug)]
enum Result {
    Win,
    Lose,
    Draw,
}

impl Result {
    fn value(&self) -> i64 {
        return match self {
            Result::Win => 6,
            Result::Lose => 0,
            Result::Draw => 3,
        }
    }
}

#[derive(Debug)]
struct Round {
    oponent: Hand,
    me: (Hand, Result),
}

impl Round {
    fn score_play(&self) -> i64 {
        let result = if self.oponent == self.me.0 {
            Result::Draw
        } else if self.oponent.beats() == self.me.0 {
            Result::Lose
        } else {
            Result::Win
        };
        return result.value() + self.me.0.value();
    }

    fn score_result(&self) -> i64 {
        let hand = match self.me.1 {
            Result::Draw => self.oponent.clone(),
            Result::Lose => self.oponent.beats().clone(),
            Result::Win => self.oponent.loses().clone(),
        };
        return hand.value() + self.me.1.value();
    }
}

fn main() {
    let rounds = reader::read(|line| {
        let (oponent, me) = line.split_once(" ").unwrap();
        Round {
            oponent: match oponent {
                "A" => Hand::Rock,
                "B" => Hand::Paper,
                "C" => Hand::Scissors,
                _ => panic!("Unknown oppenent value {}", oponent),
            },
            me: match me {
                "X" => (Hand::Rock, Result::Lose),
                "Y" => (Hand::Paper, Result::Draw),
                "Z" => (Hand::Scissors, Result::Win),
                _ => panic!("Unknown me value {}", me)
            },
        }
    });

    answer::part1(9651, rounds.iter().map(|round| round.score_play()).sum());
    answer::part2(10560, rounds.iter().map(|round| round.score_result()).sum());
}
