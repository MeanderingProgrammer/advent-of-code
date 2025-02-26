use aoc::{HashMap, HashSet, Point, Reader, answer};
use std::str::FromStr;

#[derive(Debug)]
struct Claim {
    id: usize,
    point: Point,
    width: i32,
    height: i32,
}

impl FromStr for Claim {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // #123 @ 3,2: 5x4
        let s = &s[1..];
        let (id_point, dimensions) = s.split_once(": ").unwrap();
        let (id, point) = id_point.split_once(" @ ").unwrap();
        let (width, height) = dimensions.split_once('x').unwrap();
        Ok(Self {
            id: id.parse().unwrap(),
            point: point.parse().unwrap(),
            width: width.parse().unwrap(),
            height: height.parse().unwrap(),
        })
    }
}

impl Claim {
    fn points(&self) -> Vec<Point> {
        let mut result = Vec::default();
        for x in 0..self.width {
            for y in 0..self.height {
                result.push(self.point.add(Point::new(x, y)));
            }
        }
        result
    }
}

#[derive(Debug, Default)]
struct Overlaps {
    claims: HashSet<usize>,
    points: HashSet<Point>,
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let claims = Reader::default().lines::<Claim>();
    let ids: HashSet<usize> = claims.iter().map(|claim| claim.id).collect();
    let result = overlaps(&claims);
    answer::part1(120408, result.points.len());
    answer::part2(1276, *ids.difference(&result.claims).next().unwrap());
}

fn overlaps(claims: &[Claim]) -> Overlaps {
    let mut result = Overlaps::default();
    let mut seen: HashMap<Point, usize> = HashMap::default();
    for claim in claims {
        for point in claim.points() {
            match seen.get(&point) {
                None => {
                    seen.insert(point, claim.id);
                }
                Some(id) => {
                    result.claims.insert(*id);
                    result.claims.insert(claim.id);
                    result.points.insert(point);
                }
            }
        }
    }
    result
}
