use aoc_lib::answer;
use aoc_lib::point::Point3d;
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;

#[derive(Debug, Clone)]
struct Particle {
    id: usize,
    position: Point3d,
    velocity: Point3d,
    acceleration: Point3d,
}

impl Particle {
    fn from_str(id: usize, s: &str) -> Self {
        fn parse_point(s: &str) -> Point3d {
            // _=<-119,22,36>
            s[3..s.len() - 1].parse().unwrap()
        }
        // p=<point>, v=<point>, a=<point>
        let points: Vec<&str> = s.split(", ").collect();
        Self {
            id,
            position: parse_point(points[0]),
            velocity: parse_point(points[1]),
            acceleration: parse_point(points[2]),
        }
    }

    fn step(&self) -> Self {
        let velocity = self.velocity.add(&self.acceleration);
        Self {
            id: self.id,
            position: self.position.add(&velocity),
            velocity,
            acceleration: self.acceleration.clone(),
        }
    }

    fn size(&self) -> i64 {
        self.position.length()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let particles: Vec<Particle> = Reader::default()
        .read_lines()
        .into_iter()
        .enumerate()
        .map(|(i, line)| Particle::from_str(i, &line))
        .collect();
    answer::part1(161, run_simulation(particles.clone(), false)[0].id);
    answer::part2(438, run_simulation(particles.clone(), true).len());
}

fn run_simulation(mut particles: Vec<Particle>, cleanup: bool) -> Vec<Particle> {
    for _ in 0..1_000 {
        let mut seen: FxHashSet<Point3d> = FxHashSet::default();
        let mut bad_positions: FxHashSet<Point3d> = FxHashSet::default();
        let mut next_particles: Vec<Particle> = Vec::new();
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
