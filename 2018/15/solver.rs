use aoc::prelude::*;
use rayon::prelude::*;
use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
enum Team {
    Elf,
    Goblin,
}

impl Team {
    fn enemy(&self) -> Team {
        match self {
            Self::Elf => Self::Goblin,
            Self::Goblin => Self::Elf,
        }
    }
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

impl Unit {
    fn hit(&mut self, damage: u8) {
        if self.hp <= damage {
            self.hp = 0;
        } else {
            self.hp -= damage;
        }
    }
}

#[derive(Debug, PartialEq)]
enum Status {
    Continue,
    Fail,
    Success,
}

#[derive(Debug, Clone)]
struct Game {
    units: HashMap<Point, Unit>,
    walkable: HashSet<Point>,
}

impl From<Grid<char>> for Game {
    fn from(grid: Grid<char>) -> Self {
        let mut units = HashMap::default();
        let mut walkable = HashSet::from_iter(grid.values(&'.'));
        for (tile, team) in [('G', Team::Goblin), ('E', Team::Elf)] {
            for point in grid.values(&tile) {
                units.insert(point.clone(), team.clone().into());
                walkable.insert(point);
            }
        }
        Self { units, walkable }
    }
}

impl Game {
    fn buff_team(&mut self, team: Team, amount: u8) {
        for unit in self.units.values_mut().filter(|unit| unit.team == team) {
            unit.damage += amount;
        }
    }

    fn play(&mut self, losses: bool) -> Option<i64> {
        let mut rounds = 0;
        loop {
            match self.round(losses) {
                Status::Continue => rounds += 1,
                Status::Fail => return None,
                Status::Success => {
                    let hp: i64 = self.units.values().map(|unit| unit.hp as i64).sum();
                    return Some(rounds * hp);
                }
            }
        }
    }

    fn round(&mut self, losses: bool) -> Status {
        let mut order: Vec<Point> = self.units.keys().cloned().collect();
        order.sort_unstable_by_key(|point| (point.y, point.x));
        for point in order {
            let Some(unit) = self.units.get(&point) else {
                continue;
            };
            let (enemy, damage) = (unit.team.enemy(), unit.damage);
            if self.on(&enemy).count() == 0 {
                return Status::Success;
            }
            let point = self
                .find_target(&point, &enemy)
                .or_else(|| self.make_move(&point, &enemy));
            if let Some(point) = point {
                let unit = self.units.get_mut(&point).unwrap();
                unit.hit(damage);
                if unit.hp == 0 {
                    if !losses && unit.team == Team::Elf {
                        return Status::Fail;
                    }
                    self.units.remove(&point).unwrap();
                }
            }
        }
        Status::Continue
    }

    fn on(&self, team: &Team) -> impl Iterator<Item = &Point> {
        self.units
            .iter()
            .filter(|(_, unit)| unit.team == *team)
            .map(|(point, _)| point)
    }

    fn find_target(&self, point: &Point, team: &Team) -> Option<Point> {
        point
            .neighbors()
            .into_iter()
            .flat_map(|target| self.units.get(&target).map(|unit| (target, unit)))
            .filter(|(_, unit)| unit.team == *team)
            .min_by_key(|(target, unit)| (unit.hp, target.y, target.x))
            .map(|(target, _)| target)
    }

    fn make_move(&mut self, start: &Point, team: &Team) -> Option<Point> {
        let distances = self.distances(start);

        let closest = self
            .on(team)
            .flat_map(|point| point.neighbors())
            .flat_map(|point| distances.get(&point).map(|distance| (point, distance.1)))
            .min_by_key(|(point, distance)| (*distance, point.y, point.x))?;

        let mut closest = &closest;
        while distances[&closest.0].1 > 1 {
            closest = &distances[&closest.0];
        }

        let end = closest.0.clone();
        let unit = self.units.remove(start).unwrap();
        self.units.insert(end.clone(), unit);
        self.find_target(&end, team)
    }

    fn distances(&self, point: &Point) -> HashMap<Point, (Point, u16)> {
        let mut result = HashMap::default();
        let mut queue = VecDeque::from([(point.clone(), point.clone(), 0)]);
        while let Some((child, parent, length)) = queue.pop_front() {
            if result.contains_key(&child) {
                continue;
            }
            for point in child.neighbors() {
                if self.available(&point) && !result.contains_key(&point) {
                    queue.push_back((point, child.clone(), length + 1));
                }
            }
            result.insert(child, (parent, length));
        }
        result
    }

    fn available(&self, point: &Point) -> bool {
        self.walkable.contains(point) && !self.units.contains_key(point)
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
    game.buff_team(Team::Elf, extra);
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
