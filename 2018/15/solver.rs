use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use fxhash::{FxHashMap, FxHashSet};
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
enum Team {
    Goblin,
    Elf,
}

#[derive(Debug, Clone)]
struct Character {
    team: Team,
    damage: i16,
    hp: i16,
}

impl Character {
    fn new(team: Team, extra: i16) -> Self {
        Self {
            team,
            damage: 3 + extra,
            hp: 200,
        }
    }
}

#[derive(Debug, PartialEq)]
enum Status {
    InProgress,
    Success,
    Fail,
}

#[derive(Debug)]
struct Game {
    characters: FxHashMap<Point, Character>,
    open: FxHashSet<Point>,
    no_losses: bool,
}

impl Game {
    fn new(grid: &Grid<char>, extra: i16, no_losses: bool) -> Self {
        let mut game = Self {
            characters: FxHashMap::default(),
            open: grid.values(&'.').into_iter().collect(),
            no_losses,
        };
        game.add(grid.values(&'G'), Character::new(Team::Goblin, 0));
        game.add(grid.values(&'E'), Character::new(Team::Elf, extra));
        game
    }

    fn add(&mut self, positions: Vec<Point>, character: Character) {
        positions.into_iter().for_each(|position| {
            self.characters.insert(position.clone(), character.clone());
            self.open.insert(position.clone());
        });
    }

    fn play(&mut self) -> Option<i64> {
        let (mut round, mut status) = (0, Status::InProgress);
        while status == Status::InProgress {
            status = self.round();
            round += 1;
        }
        match status {
            Status::InProgress | Status::Fail => None,
            Status::Success => {
                let hp: i64 = self
                    .characters
                    .values()
                    .map(|character| character.hp as i64)
                    .sum();
                Some((round - 1) * hp)
            }
        }
    }

    fn round(&mut self) -> Status {
        let mut positions: Vec<Point> = self.characters.keys().cloned().collect();
        positions.sort();

        for position in positions {
            let status = match self.characters.get(&position) {
                None => Status::InProgress,
                Some(character) => self.step(&position, character.clone()),
            };
            if status != Status::InProgress {
                return status;
            }
        }
        Status::InProgress
    }

    fn step(&mut self, position: &Point, character: Character) -> Status {
        if self.opponents(&character).count() == 0 {
            return Status::Success;
        }
        match self.execute(position, &character) {
            None => Status::InProgress,
            Some(position) => {
                let target = self.characters.get_mut(&position).unwrap();
                target.hp -= character.damage;
                if target.hp <= 0 {
                    let target = self.characters.remove(&position).unwrap();
                    if self.no_losses && target.team == Team::Elf {
                        return Status::Fail;
                    }
                }
                Status::InProgress
            }
        }
    }

    fn opponents<'a>(&'a self, character: &'a Character) -> impl Iterator<Item = &'a Point> {
        self.characters
            .iter()
            .filter(|(_, opponent)| opponent.team != character.team)
            .map(|(position, _)| position)
    }

    fn execute(&mut self, start: &Point, character: &Character) -> Option<Point> {
        match self.target(start, character) {
            Some(target) => Some(target),
            None => match self.make_move(start, character) {
                None => None,
                Some(end) => {
                    let target = self.target(&end, character);
                    let character = self.characters.remove(start).unwrap();
                    self.characters.insert(end, character);
                    target
                }
            },
        }
    }

    fn target(&self, position: &Point, character: &Character) -> Option<Point> {
        let neighbors = position.neighbors();
        self.opponents(character)
            .filter(|opponent| neighbors.contains(opponent))
            .map(|opponent| (self.characters.get(opponent).unwrap().hp, opponent))
            .min()
            .map(|(_, target)| target.clone())
    }

    fn make_move(&self, start: &Point, character: &Character) -> Option<Point> {
        let distances = self.distances(start);
        let closest: Option<(u16, Point)> = self
            .opponents(character)
            .flat_map(|opponent| opponent.neighbors())
            .filter(|target| distances.contains_key(target))
            .map(|target| (distances[&target].0, target))
            .min();
        match closest {
            None => None,
            Some(closest) => {
                let mut closest = &closest;
                while distances.get(&closest.1).unwrap().0 > 1 {
                    closest = distances.get(&closest.1).unwrap();
                }
                Some(closest.1.clone())
            }
        }
    }

    fn distances(&self, start: &Point) -> FxHashMap<Point, (u16, Point)> {
        let mut queue = VecDeque::default();
        queue.push_back((start.clone(), 0, start.clone()));
        let mut distances = FxHashMap::default();
        while !queue.is_empty() {
            let (position, length, parent) = queue.pop_front().unwrap();
            if !distances.contains_key(&position) {
                distances.insert(position.clone(), (length, parent.clone()));
                position
                    .neighbors()
                    .into_iter()
                    .filter(|neighbor| self.open.contains(neighbor))
                    .filter(|neighbor| !self.characters.contains_key(neighbor))
                    .filter(|neighbor| !distances.contains_key(neighbor))
                    .for_each(|neighbor| queue.push_back((neighbor, length + 1, position.clone())));
            }
        }
        distances
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    answer::part1(214731, play(&grid, 0, false).unwrap());
    answer::part2(53222, play_until(&grid));
}

fn play(grid: &Grid<char>, extra: i16, no_losses: bool) -> Option<i64> {
    Game::new(grid, extra, no_losses).play()
}

fn play_until(grid: &Grid<char>) -> i64 {
    let batch = std::thread::available_parallelism().unwrap().get() as i16;
    let mut extra = 1;
    loop {
        let result = (extra..extra + batch)
            .into_par_iter()
            .find_map_first(|extra| play(grid, extra, true));
        if let Some(result) = result {
            return result;
        }
        extra += batch;
    }
}
