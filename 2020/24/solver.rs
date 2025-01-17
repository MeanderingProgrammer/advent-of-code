use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
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

    fn to_point(&self) -> Point {
        match self {
            Self::East => Point::new(2, 0),
            Self::West => Point::new(-2, 0),
            Self::NorthEast => Point::new(1, 1),
            Self::NorthWest => Point::new(-1, 1),
            Self::SouthEast => Point::new(1, -1),
            Self::SouthWest => Point::new(-1, -1),
        }
    }
}

#[derive(Debug, Default)]
struct Floor {
    floor: FxHashMap<Point, bool>,
}

impl Floor {
    fn follow(&mut self, path: String) {
        let mut point = Point::default();
        let path = path.replace('e', "e,").replace('w', "w,");
        for instruction in path.split(',').take_while(|value| !value.is_empty()) {
            let heading = HexHeading::from_str(instruction).unwrap();
            point = point.add(&heading.to_point());
        }
        self.flip(point);
    }

    fn transform(&mut self) {
        let mut counts = FxHashMap::default();
        for (point, tile) in self.floor.iter() {
            counts.entry(point.clone()).or_insert(0);
            if !tile {
                for neighbor in HexHeading::values()
                    .iter()
                    .map(|heading| point.add(&heading.to_point()))
                {
                    counts
                        .entry(neighbor)
                        .and_modify(|count| *count += 1)
                        .or_insert(1);
                }
            }
        }
        for (point, count) in counts.into_iter() {
            let tile = *self.floor.get(&point).unwrap_or(&true);
            let flip_counts = if tile { vec![2] } else { vec![0, 3, 4, 5, 6] };
            if flip_counts.contains(&count) {
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
