use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;
use fxhash::FxHashMap;
use priority_queue::DoublePriorityQueue;

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

#[derive(Debug, PartialEq)]
enum GameStatus {
    InProgress,
    Succcess,
    Fail,
}

#[derive(Debug)]
struct Game {
    characters: FxHashMap<Point, Character>,
    open_paths: Vec<Point>,
    until_elf_death: bool,
}

impl Game {
    fn add(&mut self, positions: Vec<Point>, character: Character) {
        positions.into_iter().for_each(|position| {
            self.characters.insert(position.clone(), character.clone());
            self.open_paths.push(position);
        });
    }

    fn play(&mut self) -> Option<i64> {
        let (mut round, mut status) = (0 as i64, GameStatus::InProgress);
        while status == GameStatus::InProgress {
            status = self.round();
            round += 1;
        }
        match status {
            GameStatus::Succcess => {
                let hp_value: i64 = self
                    .characters
                    .values()
                    .map(|character| character.hp as i64)
                    .sum();
                Some((round - 1) * hp_value)
            }
            _ => None,
        }
    }

    fn round(&mut self) -> GameStatus {
        for position in self.positions().iter() {
            let status = match self.characters.get(position) {
                Some(character) => self.single_character(position, character.clone()),
                None => GameStatus::InProgress,
            };
            if status != GameStatus::InProgress {
                return status;
            }
        }
        GameStatus::InProgress
    }

    fn single_character(&mut self, position: &Point, character: Character) -> GameStatus {
        if self.opponents(&character).is_empty() {
            return GameStatus::Succcess;
        }
        match self.execute_move(position, &character) {
            Some(target_position) => {
                let target = self.characters.get_mut(&target_position).unwrap();
                let elf_target = target.team == Team::Elf;
                target.hp -= character.damage;
                if target.hp <= 0 {
                    self.characters.remove(&target_position).unwrap();
                    if self.until_elf_death && elf_target {
                        return GameStatus::Fail;
                    }
                }
                GameStatus::InProgress
            }
            None => GameStatus::InProgress,
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

    fn opponents(&self, character: &Character) -> Vec<&Point> {
        self.characters
            .iter()
            .filter(|(_, opponent)| opponent.team != character.team)
            .map(|(position, _)| position)
            .collect()
    }

    fn execute_move(&mut self, position: &Point, character: &Character) -> Option<Point> {
        match self.adjacent_target(position, character) {
            Some(target_position) => Some(target_position),
            None => match self.find_move(position, character) {
                Some(new_position) => {
                    let target_position = self.adjacent_target(&new_position, character);
                    let value = self.characters.remove(position).unwrap();
                    self.characters.insert(new_position.clone(), value);
                    target_position
                }
                None => None,
            },
        }
    }

    fn adjacent_target(&self, position: &Point, character: &Character) -> Option<Point> {
        let neighbors = position.neighbors();
        let mut targets: Vec<(i16, &Point)> = self
            .opponents(&character)
            .into_iter()
            .filter(|opponent| neighbors.contains(opponent))
            .map(|opponent| (self.characters.get(opponent).unwrap().hp, opponent))
            .collect();
        targets.sort();
        targets.into_iter().next().map(|(_, target)| target.clone())
    }

    fn find_move(&self, position: &Point, character: &Character) -> Option<Point> {
        let distances = self.distances(position);
        let closest: Option<(u16, Point)> = self
            .opponents(character)
            .iter()
            .flat_map(|opponent| opponent.neighbors())
            .filter(|target| distances.contains_key(target))
            .map(|target| (distances.get(&target).unwrap().0, target))
            .min();
        match closest {
            Some(closest) => {
                let mut closest = &closest;
                while distances.get(&closest.1).unwrap().0 > 1 {
                    closest = distances.get(&closest.1).unwrap();
                }
                Some(closest.1.clone())
            }
            None => None,
        }
    }

    fn distances(&self, start: &Point) -> FxHashMap<Point, (u16, Point)> {
        let occupied = self.positions();
        let mut queue = DoublePriorityQueue::new();
        queue.push_decrease(start.clone(), (0, start.clone()));
        let mut distances = FxHashMap::default();
        while !queue.is_empty() {
            let (position, (length, parent)) = queue.pop_min().unwrap();
            if !distances.contains_key(&position) {
                distances.insert(position.clone(), (length, parent.clone()));
                position
                    .neighbors()
                    .into_iter()
                    .filter(|neighbor| self.open_paths.contains(neighbor))
                    .filter(|neighbor| !occupied.contains(neighbor))
                    .filter(|neighbor| !distances.contains_key(neighbor))
                    .for_each(|neighbor| {
                        queue.push_decrease(neighbor, (length + 1, position.clone()));
                    });
            }
        }
        distances
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
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
        elf_damage += 1;
    }
}

fn get_game(elf_damage: i16, until_elf_death: bool) -> Game {
    fn from_grid(grid: &Grid<char>, value: char) -> Vec<Point> {
        grid.points_with_value(value)
            .into_iter()
            .map(|point| point.clone())
            .collect()
    }
    let grid = reader::read_grid(|ch| Some(ch));
    let mut game = Game {
        characters: FxHashMap::default(),
        open_paths: from_grid(&grid, '.'),
        until_elf_death,
    };
    game.add(
        from_grid(&grid, 'G'),
        Character {
            team: Team::Goblin,
            damage: 3,
            hp: 200,
        },
    );
    game.add(
        from_grid(&grid, 'E'),
        Character {
            team: Team::Elf,
            damage: elf_damage,
            hp: 200,
        },
    );
    game
}
