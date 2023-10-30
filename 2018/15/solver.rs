use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::cmp::Ordering;
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, PartialEq)]
enum Team {
    Goblin,
    Elf,
}

#[derive(Debug, Clone)]
struct Character {
    team: Team,
    damage: u32,
    hp: i64,
}

#[derive(Debug, PartialEq)]
enum GameResult {
    InProgress,
    Done,
    Failed,
}

#[derive(Debug)]
struct Game {
    characters: HashMap<Point, Character>,
    open_paths: Vec<Point>,
    until_elf_death: bool,
}

impl Game {
    fn new(open_paths: Vec<&Point>, until_elf_death: bool) -> Self {
        Self {
            characters: HashMap::new(),
            open_paths: open_paths
                .into_iter()
                .map(|position| position.clone())
                .collect(),
            until_elf_death,
        }
    }

    fn add(&mut self, character: Character, positions: Vec<&Point>) {
        positions.into_iter().for_each(|position| {
            self.characters.insert(position.clone(), character.clone());
            self.open_paths.push(position.clone());
        });
    }

    fn play(&mut self) -> Option<i64> {
        let (mut round, mut status) = (0 as i64, GameResult::InProgress);
        while status == GameResult::InProgress {
            status = self.round();
            round += 1;
        }
        match status {
            GameResult::Failed => None,
            _ => {
                let hp_value: i64 = self.characters.values().map(|character| character.hp).sum();
                Some((round - 1) * hp_value)
            }
        }
    }

    fn round(&mut self) -> GameResult {
        let positions = self.positions();
        for position in positions.iter() {
            let game_result = match self.characters.get(position) {
                Some(character) => self.single(position, character.clone()),
                None => GameResult::InProgress,
            };
            if game_result != GameResult::InProgress {
                return game_result;
            }
        }
        GameResult::InProgress
    }

    fn single(&mut self, position: &Point, character: Character) -> GameResult {
        let opponent_positions: Vec<&Point> = self
            .characters
            .iter()
            .filter(|(_, opponent)| opponent.team != character.team)
            .map(|(opponent_position, _)| opponent_position)
            .collect();

        if opponent_positions.is_empty() {
            return GameResult::Done;
        }

        let found_target_position = match self.target_position(position, &opponent_positions) {
            Some(target_position) => Some(target_position),
            None => match self.new_position(position, &opponent_positions) {
                Some(new_position) => {
                    let target_position = self.target_position(&new_position, &opponent_positions);
                    let value = self.characters.remove(position).unwrap();
                    self.characters.insert(new_position.clone(), value);
                    target_position
                }
                None => None,
            },
        };

        match found_target_position {
            Some(target_position) => {
                let target = self.characters.get_mut(&target_position).unwrap();
                let target_team = target.team.clone();
                target.hp -= character.damage as i64;
                if target.hp <= 0 {
                    self.characters.remove(&target_position).unwrap();
                    if self.until_elf_death && target_team == Team::Elf {
                        return GameResult::Failed;
                    }
                }
                GameResult::InProgress
            }
            None => GameResult::InProgress,
        }
    }

    fn positions(&self) -> Vec<Point> {
        let mut positions: Vec<Point> = self
            .characters
            .keys()
            .map(|position| position.clone())
            .collect();
        positions.sort();
        positions
    }

    fn target_position(&self, position: &Point, opponent_positions: &Vec<&Point>) -> Option<Point> {
        let neighbors = position.neighbors();
        let mut targets: Vec<(i64, &Point)> = opponent_positions
            .into_iter()
            .filter(|opponent_position| neighbors.contains(opponent_position))
            .map(|&opponent_position| {
                (
                    self.characters.get(opponent_position).unwrap().hp,
                    opponent_position,
                )
            })
            .collect();
        targets.sort();
        targets.into_iter().next().map(|(_, target)| target.clone())
    }

    fn new_position(&self, position: &Point, opponent_positions: &Vec<&Point>) -> Option<Point> {
        let distances = self.distances(position);
        let mut targets = vec![];
        for opponent_position in opponent_positions.iter() {
            targets.extend(opponent_position.neighbors());
        }
        let mut target_distances: Vec<(u32, &Point)> = targets
            .iter()
            .filter(|target| distances.contains_key(target))
            .map(|target| (distances.get(target).unwrap().0, target))
            .collect();
        target_distances.sort();
        if target_distances.len() == 0 {
            return None;
        }
        let mut closest = target_distances.iter().next().unwrap().1;
        while distances.get(closest).unwrap().0 > 1 {
            closest = &distances.get(closest).unwrap().1;
        }
        Some(closest.clone())
    }

    fn distances(&self, start: &Point) -> HashMap<Point, (u32, Point)> {
        let occupied = self.positions();
        let mut queue = VecDeque::new();
        queue.push_back((start.clone(), 0));
        let mut distances = HashMap::new();
        distances.insert(start.clone(), (0, start.clone()));
        while !queue.is_empty() {
            let (position, length) = queue.pop_front().unwrap();
            for neighbor in position.neighbors().iter() {
                if !self.open_paths.contains(neighbor) || occupied.contains(neighbor) {
                    continue;
                }
                if !distances.contains_key(neighbor) {
                    queue.push_back((neighbor.clone(), length + 1));
                }
                let parent_distance = (length + 1, position.clone());
                let should_add = match distances.get(neighbor) {
                    Some(existing) => existing.cmp(&parent_distance) == Ordering::Greater,
                    None => true,
                };
                if should_add {
                    distances.insert(neighbor.clone(), parent_distance);
                }
            }
        }
        distances
    }
}

fn main() {
    answer::part1(214731, play_game(false));
    answer::part2(53222, play_game(true));
}

fn play_game(until_elf_death: bool) -> i64 {
    let mut elf_damage = 3;
    loop {
        let mut game = get_game(elf_damage, until_elf_death);
        let result = game.play();
        if result.is_some() {
            return result.unwrap();
        }
        elf_damage += 1
    }
}

fn get_game(elf_damage: u32, until_elf_death: bool) -> Game {
    let grid = reader::read_grid(|ch| Some(ch));
    let goblin = Character {
        team: Team::Goblin,
        damage: 3,
        hp: 200,
    };
    let elf = Character {
        team: Team::Elf,
        damage: elf_damage,
        hp: 200,
    };
    let mut game = Game::new(grid.points_with_value('.'), until_elf_death);
    game.add(goblin, grid.points_with_value('G'));
    game.add(elf, grid.points_with_value('E'));
    game
}
