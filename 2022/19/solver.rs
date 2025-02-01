use aoc::{answer, Reader};
use std::str::FromStr;

#[derive(Debug)]
enum Robot {
    Ore,
    Clay,
    Obsidian,
    Geode,
}

#[derive(Debug, Clone, Default)]
struct Mineral {
    ore: u8,
    clay: u8,
    obsidian: u8,
    geode: u8,
}

impl From<Robot> for Mineral {
    fn from(value: Robot) -> Self {
        match value {
            Robot::Ore => Self::new(1, 0, 0, 0),
            Robot::Clay => Self::new(0, 1, 0, 0),
            Robot::Obsidian => Self::new(0, 0, 1, 0),
            Robot::Geode => Self::new(0, 0, 0, 1),
        }
    }
}

impl Mineral {
    fn new(ore: u8, clay: u8, obsidian: u8, geode: u8) -> Self {
        Self {
            ore,
            clay,
            obsidian,
            geode,
        }
    }

    fn add(&self, rhs: &Self) -> Self {
        Self::new(
            self.ore + rhs.ore,
            self.clay + rhs.clay,
            self.obsidian + rhs.obsidian,
            self.geode + rhs.geode,
        )
    }

    fn sub(&self, rhs: &Self) -> Self {
        Self::new(
            self.ore - rhs.ore,
            self.clay - rhs.clay,
            self.obsidian - rhs.obsidian,
            self.geode - rhs.geode,
        )
    }
}

#[derive(Debug, Clone)]
struct State {
    robots: Mineral,
    resources: Mineral,
}

impl State {
    fn can_build(&self, cost: &Mineral) -> bool {
        let have = &self.resources;
        have.ore >= cost.ore && have.clay >= cost.clay && have.obsidian >= cost.obsidian
    }

    fn next(&mut self) {
        self.resources = self.resources.add(&self.robots);
    }

    fn geodes(&self, time: u8) -> u8 {
        self.resources.geode + self.robots.geode * time
    }
}

#[derive(Debug)]
struct Blueprint {
    id: usize,
    max_ore: u8,
    max_clay: u8,
    max_obsidian: u8,
    ore_cost: Mineral,
    clay_cost: Mineral,
    obsidian_cost: Mineral,
    geode_cost: Mineral,
}

impl FromStr for Blueprint {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Blueprint 1:
        //  Each ore robot costs 4 ore.
        //  Each clay robot costs 2 ore.
        //  Each obsidian robot costs 3 ore and 14 clay.
        //  Each geode robot costs 2 ore and 7 obsidian.
        let (id, minerals) = s.split_once(": ").unwrap();
        let (_, id) = id.split_once(' ').unwrap();
        let minerals: Vec<u8> = minerals
            .split_whitespace()
            .filter_map(|s| s.parse().ok())
            .collect();

        assert_eq!(6, minerals.len());
        let [ore1, ore2, ore3, clay, ore4, obsidian] = <[u8; 6]>::try_from(&minerals[..]).unwrap();
        Ok(Self {
            id: id.parse().unwrap(),
            max_ore: ore1.max(ore2).max(ore3).max(ore4),
            max_clay: clay,
            max_obsidian: obsidian,
            ore_cost: Mineral::new(ore1, 0, 0, 0),
            clay_cost: Mineral::new(ore2, 0, 0, 0),
            obsidian_cost: Mineral::new(ore3, clay, 0, 0),
            geode_cost: Mineral::new(ore4, 0, obsidian, 0),
        })
    }
}

impl Blueprint {
    fn maximize(&self, time: u8) -> usize {
        let state = State {
            robots: Robot::Ore.into(),
            resources: Mineral::default(),
        };
        self.dfs(state, time, 0) as usize
    }

    fn dfs(&self, state: State, time: u8, result: u8) -> u8 {
        let mut result = result.max(state.geodes(time));
        if self.max_geodes(&state, time) > result {
            result = result.max(self.next(&state, time, result, Robot::Geode));
            if state.robots.obsidian < self.max_obsidian {
                result = result.max(self.next(&state, time, result, Robot::Obsidian))
            }
            if state.robots.ore < self.max_ore {
                result = result.max(self.next(&state, time, result, Robot::Ore));
            }
            if state.robots.clay < self.max_clay {
                result = result.max(self.next(&state, time, result, Robot::Clay));
            }
        }
        result
    }

    fn max_geodes(&self, state: &State, time: u8) -> u8 {
        let mut state = state.clone();
        for _ in 0..time {
            state.resources.ore = self.max_ore;
            if state.can_build(self.cost(&Robot::Geode)) {
                state = self.build(state, Robot::Geode);
            } else if state.can_build(self.cost(&Robot::Obsidian)) {
                state = self.build(state, Robot::Obsidian);
            } else {
                state.next();
            }
            state.robots = state.robots.add(&Robot::Clay.into());
        }
        state.resources.geode
    }

    fn next(&self, state: &State, time: u8, result: u8, robot: Robot) -> u8 {
        let mut time = time - 1;
        let mut state = state.clone();
        let cost = self.cost(&robot);
        while time > 0 && !state.can_build(cost) {
            time -= 1;
            state.next();
        }
        if time > 0 {
            self.dfs(self.build(state, robot), time, result)
        } else {
            result
        }
    }

    fn build(&self, mut state: State, robot: Robot) -> State {
        let cost = self.cost(&robot);
        state.next();
        state.resources = state.resources.sub(cost);
        state.robots = state.robots.add(&robot.into());
        state
    }

    fn cost(&self, robot: &Robot) -> &Mineral {
        match robot {
            Robot::Ore => &self.ore_cost,
            Robot::Clay => &self.clay_cost,
            Robot::Obsidian => &self.obsidian_cost,
            Robot::Geode => &self.geode_cost,
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let bps: Vec<Blueprint> = Reader::default().read_from_str();
    answer::part1(1599, bps.iter().map(|bp| bp.maximize(24) * bp.id).sum());
    answer::part2(
        14112,
        bps.iter().take(3).map(|bp| bp.maximize(32)).product(),
    );
}
