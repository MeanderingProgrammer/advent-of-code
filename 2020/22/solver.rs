use aoc::{HashSet, Reader, answer};
use std::collections::VecDeque;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Deck {
    cards: VecDeque<u8>,
}

impl FromStr for Deck {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let cards = s
            .lines()
            .skip(1)
            .map(|value| value.parse().unwrap())
            .collect();
        Ok(Self { cards })
    }
}

impl Deck {
    fn len(&self) -> u8 {
        self.cards.len() as u8
    }

    fn empty(&self) -> bool {
        self.cards.is_empty()
    }

    fn next(&mut self) -> u8 {
        self.cards.pop_front().unwrap()
    }

    fn add(&mut self, card1: u8, card2: u8) {
        self.cards.push_back(card1);
        self.cards.push_back(card2);
    }

    fn split(&self, index: u8) -> Self {
        let cards = self.cards.iter().take(index as usize).copied().collect();
        Self { cards }
    }

    fn score(&self) -> usize {
        self.cards
            .iter()
            .enumerate()
            .map(|(i, &card)| (self.cards.len() - i) * (card as usize))
            .sum()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Decks(Deck, Deck);

impl Decks {
    fn done(&self) -> bool {
        self.0.empty() || self.1.empty()
    }

    fn next(&mut self) -> (u8, u8) {
        (self.0.next(), self.1.next())
    }

    fn can_split(&self, i1: u8, i2: u8) -> bool {
        i1 <= self.0.len() && i2 <= self.1.len()
    }

    fn split(&self, i1: u8, i2: u8) -> Self {
        Self(self.0.split(i1), self.1.split(i2))
    }
}

#[derive(Debug)]
enum Player {
    One,
    Two,
}

#[derive(Debug, Clone)]
struct Game {
    decks: Decks,
    states: HashSet<Decks>,
}

impl Game {
    fn new(decks: Decks) -> Self {
        Self {
            decks,
            states: HashSet::default(),
        }
    }

    fn play(&mut self, recursize: bool) -> Player {
        while !self.decks.done() {
            if !self.states.insert(self.decks.clone()) {
                return Player::One;
            }
            self.next(recursize);
        }
        if !self.decks.0.empty() {
            Player::One
        } else {
            Player::Two
        }
    }

    fn next(&mut self, recursize: bool) {
        let (card1, card2) = self.decks.next();
        let winner = if recursize && self.decks.can_split(card1, card2) {
            Self::new(self.decks.split(card1, card2)).play(recursize)
        } else if card1 > card2 {
            Player::One
        } else {
            Player::Two
        };
        match winner {
            Player::One => self.decks.0.add(card1, card2),
            Player::Two => self.decks.1.add(card2, card1),
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let decks = Reader::default().groups::<Deck>();
    let game = Game::new(Decks(decks[0].clone(), decks[1].clone()));
    answer::part1(32102, play(&game, false));
    answer::part2(34173, play(&game, true));
}

fn play(game: &Game, recursize: bool) -> usize {
    let mut game = game.clone();
    let deck = match game.play(recursize) {
        Player::One => &game.decks.0,
        Player::Two => &game.decks.1,
    };
    deck.score()
}
