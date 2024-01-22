use aoc_lib::answer;
use aoc_lib::point::Point3d;
use aoc_lib::reader::Reader;
use nom::{
    bytes::complete::tag,
    character::complete::digit0,
    combinator::{map_res, opt},
    sequence::tuple,
    IResult,
};
use std::collections::HashSet;

#[derive(Debug, Clone)]
struct Particle {
    id: usize,
    acceleration: Point3d,
    velocity: Point3d,
    position: Point3d,
}

impl Particle {
    fn from_str(id: usize, input: &str) -> IResult<&str, Self> {
        fn parse_number(input: &str) -> IResult<&str, i64> {
            map_res(
                tuple((opt(tag("-")), digit0)),
                |(sign, s): (Option<&str>, &str)| (sign.unwrap_or("").to_string() + s).parse(),
            )(input)
        }

        fn parse_point(input: &str) -> IResult<&str, Point3d> {
            // <-119,22,36>
            let (input, _) = tag("<")(input)?;
            let (input, x) = parse_number(input)?;
            let (input, _) = tag(",")(input)?;
            let (input, y) = parse_number(input)?;
            let (input, _) = tag(",")(input)?;
            let (input, z) = parse_number(input)?;
            let (input, _) = tag(">")(input)?;
            Ok((input, Point3d::new(x, y, z)))
        }

        // p=<point>, v=<point>, a=<point>
        let (input, _) = tag("p=")(input)?;
        let (input, position) = parse_point(input)?;
        let (input, _) = tag(", v=")(input)?;
        let (input, velocity) = parse_point(input)?;
        let (input, _) = tag(", a=")(input)?;
        let (input, acceleration) = parse_point(input)?;

        Ok((
            input,
            Self {
                id,
                acceleration,
                velocity,
                position,
            },
        ))
    }

    fn step(&self) -> Self {
        let velocity = &self.velocity + &self.acceleration;
        let position = &self.position + &velocity;
        Self {
            id: self.id,
            acceleration: self.acceleration.clone(),
            velocity,
            position,
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
        .map(|(i, line)| Particle::from_str(i, &line).unwrap().1)
        .collect();
    answer::part1(161, run_simulation(particles.clone(), false)[0].id);
    answer::part2(438, run_simulation(particles.clone(), true).len());
}

fn run_simulation(mut particles: Vec<Particle>, cleanup: bool) -> Vec<Particle> {
    for _ in 0..1_000 {
        let mut seen: HashSet<Point3d> = HashSet::new();
        let mut bad_positions: HashSet<Point3d> = HashSet::new();
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
