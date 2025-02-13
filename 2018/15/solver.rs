use aoc::{answer, Grid, HashMap, HashSet, Point, Reader};
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
enum Team {
    Goblin,
    Elf,
}

#[derive(Debug, Clone)]
struct Unit {
    team: Team,
    damage: u8,
    hp: u8,
}

impl From<Team> for Unit {
    fn from(team: Team) -> Self {
        Self {
            team,
            damage: 3,
            hp: 200,
        }
    }
}

#[derive(Debug, PartialEq)]
enum Status {
    Running,
    Success,
    Fail,
}

#[derive(Debug, Clone)]
struct Game {
    units: HashMap<Point, Unit>,
    space: HashSet<Point>,
}

impl From<Grid<char>> for Game {
    fn from(grid: Grid<char>) -> Self {
        let mut game = Self {
            units: HashMap::default(),
            space: grid.values(&'.').into_iter().collect(),
        };
        game.add(grid.values(&'G'), Team::Goblin);
        game.add(grid.values(&'E'), Team::Elf);
        game
    }
}

impl Game {
    fn add(&mut self, positions: Vec<Point>, team: Team) {
        positions.into_iter().for_each(|position| {
            self.units.insert(position.clone(), team.clone().into());
            self.space.insert(position);
        });
    }

    fn buff(&mut self, team: Team, amount: u8) {
        for (_, unit) in self.units.iter_mut() {
            if unit.team == team {
                unit.damage += amount;
            }
        }
    }

    fn play(&mut self, losses: bool) -> Option<i64> {
        let (mut round, mut status) = (0, Status::Running);
        while status == Status::Running {
            status = self.round(losses);
            round += 1;
        }
        match status {
            Status::Fail => None,
            Status::Success => {
                let hp: i64 = self.units.values().map(|unit| unit.hp as i64).sum();
                Some((round - 1) * hp)
            }
            Status::Running => unreachable!(),
        }
    }

    fn round(&mut self, losses: bool) -> Status {
        let mut positions: Vec<Point> = self.units.keys().cloned().collect();
        positions.sort_by_key(|point| (point.y, point.x));
        for position in positions {
            if let Some(unit) = self.units.get(&position) {
                if self.opponents(unit).count() == 0 {
                    return Status::Success;
                } else if let Some(killed) = self.step(&position, unit.clone()) {
                    if !losses && killed.team == Team::Elf {
                        return Status::Fail;
                    }
                }
            }
        }
        Status::Running
    }

    fn opponents<'a>(&'a self, unit: &'a Unit) -> impl Iterator<Item = &'a Point> {
        self.units
            .iter()
            .filter(|(_, opponent)| opponent.team != unit.team)
            .map(|(position, _)| position)
    }

    fn step(&mut self, position: &Point, unit: Unit) -> Option<Unit> {
        match self.execute(position, &unit) {
            None => None,
            Some(position) => {
                let target = self.units.get_mut(&position).unwrap();
                if target.hp > unit.damage {
                    target.hp -= unit.damage;
                    None
                } else {
                    self.units.remove(&position)
                }
            }
        }
    }

    fn execute(&mut self, start: &Point, unit: &Unit) -> Option<Point> {
        match self.target(start, unit) {
            Some(target) => Some(target),
            None => match self.make_move(start, unit) {
                None => None,
                Some(end) => {
                    let target = self.target(&end, unit);
                    let unit = self.units.remove(start).unwrap();
                    self.units.insert(end, unit);
                    target
                }
            },
        }
    }

    fn target(&self, position: &Point, unit: &Unit) -> Option<Point> {
        let neighbors = position.neighbors();
        self.opponents(unit)
            .filter(|opponent| neighbors.contains(opponent))
            .map(|opponent| (self.units[opponent].hp, opponent))
            .min_by_key(|(hp, target)| (*hp, target.y, target.x))
            .map(|(_, target)| target.clone())
    }

    fn make_move(&self, start: &Point, unit: &Unit) -> Option<Point> {
        let distances = self.distances(start);
        let closest: Option<(u16, Point)> = self
            .opponents(unit)
            .flat_map(|opponent| opponent.neighbors())
            .filter(|target| distances.contains_key(target))
            .map(|target| (distances[&target].0, target))
            .min_by_key(|(distance, target)| (*distance, target.y, target.x));
        match closest {
            None => None,
            Some(closest) => {
                let mut closest = &closest;
                while distances[&closest.1].0 > 1 {
                    closest = &distances[&closest.1];
                }
                Some(closest.1.clone())
            }
        }
    }

    fn distances(&self, start: &Point) -> HashMap<Point, (u16, Point)> {
        let mut queue = VecDeque::default();
        queue.push_back((start.clone(), 0, start.clone()));
        let mut distances = HashMap::default();
        while !queue.is_empty() {
            let (position, length, parent) = queue.pop_front().unwrap();
            if distances.contains_key(&position) {
                continue;
            }
            distances.insert(position.clone(), (length, parent.clone()));
            position
                .neighbors()
                .into_iter()
                .filter(|neighbor| self.space.contains(neighbor))
                .filter(|neighbor| !self.units.contains_key(neighbor))
                .filter(|neighbor| !distances.contains_key(neighbor))
                .for_each(|neighbor| queue.push_back((neighbor, length + 1, position.clone())));
        }
        distances
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    let game = grid.into();
    answer::part1(214731, play(&game, 0, true).unwrap());
    answer::part2(53222, play_until(&game));
}

fn play(game: &Game, extra: u8, losses: bool) -> Option<i64> {
    let mut game = game.clone();
    game.buff(Team::Elf, extra);
    game.play(losses)
}

fn play_until(game: &Game) -> i64 {
    let batch = std::thread::available_parallelism().unwrap().get() as u8;
    let mut extra = 1;
    loop {
        let result = (extra..extra + batch)
            .into_par_iter()
            .find_map_first(|extra| play(game, extra, false));
        if let Some(result) = result {
            return result;
        }
        extra += batch;
    }
}
