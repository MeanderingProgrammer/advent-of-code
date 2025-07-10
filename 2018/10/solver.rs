use aoc::prelude::*;
use std::str::FromStr;

#[derive(Debug)]
struct Particle {
    position: Point,
    velocity: Point,
}

impl FromStr for Particle {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // position=<point> velocity=<point>
        let (position, velocity) = s.split_at(25);
        Ok(Self {
            position: position.parse().unwrap(),
            velocity: velocity.parse().unwrap(),
        })
    }
}

impl Particle {
    fn at(&self, time: i32) -> Point {
        self.position.add(self.velocity.mul(time))
    }
}

#[derive(Debug)]
struct Particles {
    particles: Vec<Particle>,
}

impl Particles {
    fn min_area(&self) -> Option<i32> {
        let mut previous = self.area_at(0);
        for time in 1.. {
            let area = self.area_at(time);
            if area > previous {
                return Some(time - 1);
            }
            previous = area;
        }
        None
    }

    fn area_at(&self, time: i32) -> i64 {
        let positions = self.at(time);
        let bounds = Bounds::new(&positions);
        let dx = (bounds.upper.x - bounds.lower.x) as i64;
        let dy = (bounds.upper.y - bounds.lower.y) as i64;
        dy * dx
    }

    fn at(&self, time: i32) -> Vec<Point> {
        self.particles
            .iter()
            .map(|particle| particle.at(time))
            .collect()
    }

    fn grid_str(&self, time: i32) -> String {
        let mut grid: Grid<char> = Grid::default();
        self.at(time).into_iter().for_each(|position| {
            grid.add(position, '#');
        });
        grid.to_string()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let particles = Reader::default().lines();
    let particles = Particles { particles };
    let time = particles.min_area().unwrap();
    let expected = [
        ".####...#####......###..#.......#.......#.......#.......#....#",
        "#....#..#....#......#...#.......#.......#.......#.......#....#",
        "#.......#....#......#...#.......#.......#.......#.......#....#",
        "#.......#....#......#...#.......#.......#.......#.......#....#",
        "#.......#####.......#...#.......#.......#.......#.......######",
        "#..###..#...........#...#.......#.......#.......#.......#....#",
        "#....#..#...........#...#.......#.......#.......#.......#....#",
        "#....#..#.......#...#...#.......#.......#.......#.......#....#",
        "#...##..#.......#...#...#.......#.......#.......#.......#....#",
        ".###.#..#........###....######..######..######..######..#....#",
    ];
    answer::part1(
        "\n".to_owned() + &expected.join("\n"),
        "\n".to_owned() + &particles.grid_str(time),
    );
    answer::part2(10515, time);
}
