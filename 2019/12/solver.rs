use aoc::{Iter, Point3d, Reader, answer, math};
use std::cmp::Ordering;
use std::str::FromStr;
use std::sync::mpsc;
use std::thread;

#[derive(Debug, Clone, Default)]
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
    fn values() -> &'static [Self] {
        &[Self::X, Self::Y, Self::Z]
    }

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
        // <x=4, y=12, z=13>
        let p: Point3d = s.parse().unwrap();
        Ok(Self {
            position: Vector(p.x as i64, p.y as i64, p.z as i64),
            velocity: Vector::default(),
        })
    }
}

impl Body {
    fn apply_gravity(&mut self, difference: &Vector) {
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
        for combination in (0..self.bodies.len()).combinations(2) {
            let (i, j) = (combination[0], combination[1]);
            let (vi, vj) = (&self.bodies[i].position, &self.bodies[j].position);
            let (diff_ij, diff_ji) = (vi.subtract(vj), vj.subtract(vi));
            self.bodies[i].apply_gravity(&diff_ij);
            self.bodies[j].apply_gravity(&diff_ji);
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
    answer::timer(solution);
}

fn solution() {
    let bodies = Reader::default().lines();
    let system = System { bodies };
    answer::part1(5350, run(system.clone(), 1_000));
    answer::part2(467034091553512, system_period(system.clone()));
}

fn run(mut system: System, n: usize) -> i64 {
    for _ in 0..n {
        system.step();
    }
    system.energy()
}

fn system_period(system: System) -> usize {
    let (tx, rx) = mpsc::channel();
    for component in Component::values() {
        let system = system.clone();
        let thread_tx = tx.clone();
        thread::spawn(move || {
            let period = component_period(system, component);
            thread_tx.send(period).unwrap();
        });
    }
    drop(tx);
    let periods = rx.iter().collect();
    math::lcm(periods)
}

fn component_period(mut system: System, component: &Component) -> usize {
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
