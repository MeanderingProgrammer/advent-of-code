use aoc_lib::answer;
use aoc_lib::reader::Reader;
use nom::{bytes::complete::tag, character::complete::digit0, IResult};
use std::collections::VecDeque;

#[derive(Debug, Default)]
struct Player {
    score: usize,
}

#[derive(Debug)]
struct Game {
    players: Vec<Player>,
    board: VecDeque<usize>,
}

impl Game {
    fn play(&mut self, moves: usize) {
        for i in 0..moves {
            let mut value = i + 1;
            if value % 23 == 0 {
                self.board.rotate_left(6);
                let index = i % self.players.len();
                let player = self.players.get_mut(index).unwrap();
                player.score += value;
                value = self.board.pop_front().unwrap();
                player.score += self.board.pop_front().unwrap();
            } else {
                self.board.rotate_right(1);
            }
            self.board.push_front(value);
        }
    }

    fn high_score(&self) -> Option<usize> {
        self.players.iter().map(|player| player.score).max()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let line = Reader::default().read_line();
    let (players, value) = parse_line(&line).unwrap().1;
    answer::part1(429943, solve(players, value));
    answer::part2(3615691746, solve(players, value * 100));
}

fn parse_line(input: &str) -> IResult<&str, (usize, usize)> {
    // <number> players; last marble is worth <number> points
    let (input, players) = digit0(input)?;
    let (input, _) = tag(" players; last marble is worth ")(input)?;
    let (input, value) = digit0(input)?;
    let (input, _) = tag(" points")(input)?;
    Ok((input, (players.parse().unwrap(), value.parse().unwrap())))
}

fn solve(players: usize, moves: usize) -> usize {
    let mut game = Game {
        players: (0..players).map(|_| Player::default()).collect(),
        board: [0].into(),
    };
    game.play(moves);
    game.high_score().unwrap()
}
