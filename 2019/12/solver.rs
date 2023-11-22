use aoc_lib::answer;
use aoc_lib::math;
use aoc_lib::reader;
use itertools::Itertools;
use regex::Regex;
use std::cmp::Ordering;
use std::str::FromStr;

#[derive(Debug, Clone)]
struct Vector(i64, i64, i64);

impl Vector {
    fn add(&self, other: &Self) -> Self {
        Self(self.0 + other.0, self.1 + other.1, self.2 + other.2)
    }

    fn subtract(&self, other: &Self) -> Self {
        Self(self.0 - other.0, self.1 - other.1, self.2 - other.2)
    }

    fn clamp(&self) -> Self {
        Self(
            Self::direction(self.0),
            Self::direction(self.1),
            Self::direction(self.2),
        )
    }

    fn direction(value: i64) -> i64 {
        match value.cmp(&0) {
            Ordering::Less => -1,
            Ordering::Equal => 0,
            Ordering::Greater => 1,
        }
    }

    fn energy(&self) -> i64 {
        self.0.abs() + self.1.abs() + self.2.abs()
    }
}

#[derive(Debug)]
enum Component {
    X,
    Y,
    Z,
}

impl Component {
    fn get(&self, vector: &Vector) -> i64 {
        match self {
            Self::X => vector.0,
            Self::Y => vector.1,
            Self::Z => vector.2,
        }
    }
}

#[derive(Debug, Clone)]
struct Body {
    position: Vector,
    velocity: Vector,
}

impl FromStr for Body {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"<x=(?P<x>.*), y=(?P<y>.*), z=(?P<z>.*)>").unwrap();
        let caps = re.captures(s).unwrap();
        let (x, y, z) = (&caps["x"], &caps["y"], &caps["z"]);
        Ok(Self {
            position: Vector(x.parse().unwrap(), y.parse().unwrap(), z.parse().unwrap()),
            velocity: Vector(0, 0, 0),
        })
    }
}

impl Body {
    fn apply_gravity(&mut self, other_position: Vector) {
        let difference = self.position.subtract(&other_position);
        self.velocity = self.velocity.subtract(&difference.clamp());
    }

    fn apply_velocity(&mut self) {
        self.position = self.position.add(&self.velocity);
    }

    fn energy(&self) -> i64 {
        self.position.energy() * self.velocity.energy()
    }

    fn extract(&self, component: &Component) -> (i64, i64) {
        (component.get(&self.position), component.get(&self.velocity))
    }
}

#[derive(Debug, Clone)]
struct System {
    bodies: Vec<Body>,
}

impl System {
    fn step(&mut self) {
        for permutation in (0..self.bodies.len()).permutations(2) {
            let (i, j) = (permutation[0], permutation[1]);
            let other_position = self.bodies[j].position.clone();
            self.bodies[i].apply_gravity(other_position);
        }
        self.bodies
            .iter_mut()
            .for_each(|body| body.apply_velocity());
    }

    fn energy(&self) -> i64 {
        self.bodies.iter().map(|body| body.energy()).sum()
    }

    fn extract(&self, component: &Component) -> Vec<(i64, i64)> {
        self.bodies
            .iter()
            .map(|body| body.extract(component))
            .collect()
    }
}

fn main() {
    let system = System {
        bodies: reader::read(|line| line.parse().unwrap()),
    };
    answer::part1(5350, run_for(system.clone(), 1_000));
    answer::part2(467034091553512, system_period(system.clone()));
}

fn run_for(mut system: System, n: usize) -> i64 {
    for _ in 0..n {
        system.step();
    }
    system.energy()
}

fn system_period(system: System) -> i64 {
    let x_period = component_period(system.clone(), &Component::X);
    let y_period = component_period(system.clone(), &Component::Y);
    let z_period = component_period(system.clone(), &Component::Z);
    math::lcm(math::lcm(x_period, y_period), z_period)
}

fn component_period(mut system: System, component: &Component) -> i64 {
    let goal = system.extract(component);
    let mut step = 0;
    loop {
        system.step();
        step += 1;
        if goal == system.extract(component) {
            return step;
        }
    }
}
