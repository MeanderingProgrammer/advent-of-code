use aoc::{answer, Bounds, HashMap, Point, Reader};

#[derive(Debug)]
struct Distance {
    infinite: bool,
    to: Vec<i32>,
}

impl Distance {
    fn closest(&self) -> Option<u8> {
        let min = self.distances().min().unwrap();
        let indexes: Vec<u8> = self
            .distances()
            .enumerate()
            .filter(|(_, distance)| *distance == min)
            .map(|(i, _)| i as u8)
            .collect();
        if indexes.len() == 1 {
            Some(indexes[0])
        } else {
            None
        }
    }

    fn total(&self) -> i32 {
        self.distances().sum()
    }

    fn distances(&self) -> impl Iterator<Item = i32> + '_ {
        self.to.iter().copied()
    }
}

#[derive(Debug)]
struct Coordinates {
    distances: Vec<Distance>,
}

impl Coordinates {
    fn new(points: Vec<Point>) -> Self {
        let bounds = Bounds::new(&points);
        Self {
            distances: (bounds.lower.x..=bounds.upper.x)
                .flat_map(|x| (bounds.lower.y..=bounds.upper.y).map(move |y| Point::new(x, y)))
                .map(|start| Distance {
                    infinite: bounds.edge(&start),
                    to: points
                        .iter()
                        .map(|end| start.manhattan_distance(end))
                        .collect(),
                })
                .collect(),
        }
    }

    fn largest_finite(&self) -> usize {
        let mut regions: HashMap<u8, Vec<bool>> = HashMap::default();
        for distance in self.distances.iter() {
            if let Some(closest) = distance.closest() {
                regions.entry(closest).or_default().push(distance.infinite);
            }
        }
        regions
            .values()
            .filter(|region| !region.iter().any(|infinite| *infinite))
            .map(|region| region.len())
            .max()
            .unwrap()
    }

    fn within(&self, max: i32) -> usize {
        // Assumes no points outside of min / max boundaries fall within
        // the max allowable distance, this assumption could be checked
        self.distances
            .iter()
            .filter(|distance| distance.total() < max)
            .count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points = Reader::default().read_from_str();
    let coordinates = Coordinates::new(points);
    answer::part1(3251, coordinates.largest_finite());
    answer::part2(47841, coordinates.within(10_000));
}
