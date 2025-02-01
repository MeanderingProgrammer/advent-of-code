use aoc_lib::answer;
use aoc_lib::collections::HashMap;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use std::str::FromStr;

#[derive(Debug)]
enum HexHeading {
    East,
    West,
    NorthEast,
    NorthWest,
    SouthEast,
    SouthWest,
}

impl FromStr for HexHeading {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "e" => Ok(Self::East),
            "w" => Ok(Self::West),
            "ne" => Ok(Self::NorthEast),
            "nw" => Ok(Self::NorthWest),
            "se" => Ok(Self::SouthEast),
            "sw" => Ok(Self::SouthWest),
            _ => Err(format!("Unknown heading: {s}")),
        }
    }
}

impl From<&HexHeading> for Point {
    fn from(value: &HexHeading) -> Self {
        match value {
            HexHeading::East => Self::new(2, 0),
            HexHeading::West => Self::new(-2, 0),
            HexHeading::NorthEast => Self::new(1, 1),
            HexHeading::NorthWest => Self::new(-1, 1),
            HexHeading::SouthEast => Self::new(1, -1),
            HexHeading::SouthWest => Self::new(-1, -1),
        }
    }
}

impl HexHeading {
    fn values() -> &'static [Self] {
        &[
            Self::East,
            Self::West,
            Self::NorthEast,
            Self::NorthWest,
            Self::SouthEast,
            Self::SouthWest,
        ]
    }
}

#[derive(Debug)]
struct Floor {
    floor: HashMap<Point, bool>,
    counts: HashMap<bool, Vec<usize>>,
}

impl Default for Floor {
    fn default() -> Self {
        Self {
            floor: HashMap::default(),
            counts: HashMap::from_iter([(true, vec![2]), (false, vec![0, 3, 4, 5, 6])]),
        }
    }
}

impl Floor {
    fn follow(&mut self, path: String) {
        let mut point = Point::default();
        let path = path.replace('e', "e,").replace('w', "w,");
        for instruction in path.split(',').take_while(|value| !value.is_empty()) {
            let heading = HexHeading::from_str(instruction).unwrap();
            point = point.add(&heading);
        }
        self.flip(point);
    }

    fn transform(&mut self) {
        let mut counts = HashMap::default();
        for (point, tile) in self.floor.iter() {
            counts.entry(point.clone()).or_insert(0);
            if !tile {
                for neighbor in HexHeading::values()
                    .iter()
                    .map(|heading| point.add(heading))
                {
                    counts
                        .entry(neighbor)
                        .and_modify(|count| *count += 1)
                        .or_insert(1);
                }
            }
        }

        for (point, count) in counts.into_iter() {
            let tile = self.floor.get(&point).unwrap_or(&true);
            if self.counts[tile].contains(&count) {
                self.flip(point);
            }
        }
    }

    fn flip(&mut self, point: Point) {
        self.floor
            .entry(point)
            .and_modify(|tile| *tile = !*tile)
            .or_insert(false);
    }

    fn black(&self) -> usize {
        self.floor.values().filter(|&&tile| !tile).count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut floor = Floor::default();
    Reader::default()
        .read_lines()
        .into_iter()
        .for_each(|path| floor.follow(path));
    let part1 = floor.black();
    (0..100).for_each(|_| floor.transform());
    answer::part1(320, part1);
    answer::part2(3777, floor.black());
}
