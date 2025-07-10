use aoc::prelude::*;

#[derive(Debug, Clone)]
struct Particle {
    id: usize,
    position: Point3d,
    velocity: Point3d,
    acceleration: Point3d,
}

impl Particle {
    fn from_str(id: usize, s: &str) -> Self {
        // p=<point>, v=<point>, a=<point>
        let [position, velocity, acceleration] = [0, 1, 2].map(|i| Str::nth(s, ' ', i));
        Self {
            id,
            position,
            velocity,
            acceleration,
        }
    }

    fn step(&self) -> Self {
        let velocity = self.velocity.add(self.acceleration.clone());
        Self {
            id: self.id,
            position: self.position.add(velocity.clone()),
            velocity,
            acceleration: self.acceleration.clone(),
        }
    }

    fn size(&self) -> i32 {
        self.position.length()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let particles = Reader::default()
        .lines::<String>()
        .into_iter()
        .enumerate()
        .map(|(i, line)| Particle::from_str(i, &line))
        .collect::<Vec<_>>();
    answer::part1(161, run_simulation(particles.clone(), false)[0].id);
    answer::part2(438, run_simulation(particles.clone(), true).len());
}

fn run_simulation(mut particles: Vec<Particle>, cleanup: bool) -> Vec<Particle> {
    for _ in 0..1_000 {
        let mut seen: HashSet<Point3d> = HashSet::default();
        let mut bad_positions: HashSet<Point3d> = HashSet::default();
        let mut next_particles: Vec<Particle> = Vec::default();
        for particle in particles.iter() {
            let next_particle = particle.step();
            if cleanup {
                let next_position = next_particle.position.clone();
                if seen.contains(&next_position) {
                    bad_positions.insert(next_position);
                } else {
                    seen.insert(next_position);
                }
            }
            next_particles.push(next_particle);
        }
        particles = next_particles
            .into_iter()
            .filter(|particle| !bad_positions.contains(&particle.position))
            .collect();
    }
    particles.sort_by_key(|a| a.size());
    particles
}
