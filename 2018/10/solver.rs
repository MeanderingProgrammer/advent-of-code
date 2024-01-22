use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use nom::{
    bytes::complete::tag,
    character::complete::{digit0, space0},
    combinator::{map_res, opt},
    sequence::tuple,
    IResult,
};

#[derive(Debug)]
struct Particle {
    position: Point,
    velocity: Point,
}

impl Particle {
    fn from_str(input: &str) -> IResult<&str, Self> {
        fn parse_number(input: &str) -> IResult<&str, i64> {
            let (input, _) = space0(input)?;
            map_res(
                tuple((opt(tag("-")), digit0)),
                |(sign, s): (Option<&str>, &str)| (sign.unwrap_or("").to_string() + s).parse(),
            )(input)
        }

        fn parse_point(input: &str) -> IResult<&str, Point> {
            // < 10749, -20904> | <-1,  2>
            let (input, _) = tag("<")(input)?;
            let (input, x) = parse_number(input)?;
            let (input, _) = tag(",")(input)?;
            let (input, y) = parse_number(input)?;
            let (input, _) = tag(">")(input)?;
            Ok((input, Point::new(x, y)))
        }

        // position=<point> velocity=<point>
        let (input, _) = tag("position=")(input)?;
        let (input, position) = parse_point(input)?;
        let (input, _) = tag(" velocity=")(input)?;
        let (input, velocity) = parse_point(input)?;

        Ok((input, Self { position, velocity }))
    }

    fn at(&self, time: i64) -> Point {
        &self.position + &(&self.velocity * time)
    }
}

#[derive(Debug)]
struct Particles {
    particles: Vec<Particle>,
}

impl Particles {
    fn min_area(&self) -> Option<i64> {
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

    fn area_at(&self, time: i64) -> i64 {
        let positions = self.at(time);
        let xs: Vec<i64> = positions.iter().map(|position| position.x).collect();
        let dx = xs.iter().max().unwrap() - xs.iter().min().unwrap();
        let ys: Vec<i64> = positions.iter().map(|position| position.y).collect();
        let dy = ys.iter().max().unwrap() - ys.iter().min().unwrap();
        dy * dx
    }

    fn at(&self, time: i64) -> Vec<Point> {
        self.particles
            .iter()
            .map(|particle| particle.at(time))
            .collect()
    }

    fn grid_str(&self, time: i64) -> String {
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
    let particles = Particles {
        particles: Reader::default().read(|line| Particle::from_str(line).unwrap().1),
    };
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
