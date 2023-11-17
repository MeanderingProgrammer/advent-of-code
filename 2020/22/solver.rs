use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::{HashSet, VecDeque};

#[derive(Debug)]
enum Player {
    One,
    Two,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Deck(VecDeque<u8>);

impl Deck {
    fn len(&self) -> u8 {
        self.0.len() as u8
    }

    fn empty(&self) -> bool {
        self.0.is_empty()
    }

    fn next(&mut self) -> u8 {
        self.0.pop_front().unwrap()
    }

    fn add(&mut self, card1: u8, card2: u8) {
        self.0.push_back(card1);
        self.0.push_back(card2);
    }

    fn split(&self, index: u8) -> Self {
        Self(
            self.0
                .iter()
                .take(index as usize)
                .map(|&value| value)
                .collect(),
        )
    }

    fn score(&self) -> usize {
        self.0
            .iter()
            .enumerate()
            .map(|(i, &card)| (self.0.len() - i) * (card as usize))
            .sum()
    }
}

#[derive(Debug)]
struct Game {
    deck1: Deck,
    deck2: Deck,
    recursize: bool,
    states: HashSet<(Deck, Deck)>,
}

impl Game {
    fn new(deck1: Deck, deck2: Deck, recursize: bool) -> Self {
        Self {
            deck1,
            deck2,
            recursize,
            states: HashSet::new(),
        }
    }
    fn play(&mut self) -> &Deck {
        match self.get_winner() {
            Player::One => &self.deck1,
            Player::Two => &self.deck2,
        }
    }

    fn get_winner(&mut self) -> Player {
        while !self.deck1.empty() && !self.deck2.empty() {
            if self.is_repeat() {
                return Player::One;
            }
            self.play_round();
        }
        if self.deck1.empty() {
            Player::Two
        } else {
            Player::One
        }
    }

    fn is_repeat(&mut self) -> bool {
        let state = (self.deck1.clone(), self.deck2.clone());
        if self.states.contains(&state) {
            true
        } else {
            self.states.insert(state);
            false
        }
    }

    fn play_round(&mut self) {
        let (card1, card2) = (self.deck1.next(), self.deck2.next());
        let winner = if self.recursize && card1 <= self.deck1.len() && card2 <= self.deck2.len() {
            Game::new(
                self.deck1.split(card1),
                self.deck2.split(card2),
                self.recursize,
            )
            .get_winner()
        } else {
            if card1 > card2 {
                Player::One
            } else {
                Player::Two
            }
        };
        match winner {
            Player::One => self.deck1.add(card1, card2),
            Player::Two => self.deck2.add(card2, card1),
        }
    }
}

fn main() {
    answer::part1(32102, play_game(false));
    answer::part2(34173, play_game(true));
}

fn play_game(recursize: bool) -> usize {
    let data = reader::read_group_lines();
    let mut game = Game::new(get_deck(&data[0]), get_deck(&data[1]), recursize);
    game.play().score()
}

fn get_deck(values: &Vec<String>) -> Deck {
    Deck(
        values
            .iter()
            .skip(1)
            .map(|value| value.parse().unwrap())
            .collect(),
    )
}
