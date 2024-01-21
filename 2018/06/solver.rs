use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;

#[derive(Debug)]
struct PointGrid {
    x_bounds: (i64, i64),
    y_bounds: (i64, i64),
    distances: FxHashMap<Point, FxHashMap<Point, i64>>,
}

impl PointGrid {
    fn new(points: Vec<Point>) -> Self {
        let xs: Vec<i64> = points.iter().map(|point| point.x).collect();
        let x_bounds = (*xs.iter().min().unwrap(), *xs.iter().max().unwrap());
        let ys: Vec<i64> = points.iter().map(|point| point.y).collect();
        let y_bounds = (*ys.iter().min().unwrap(), *ys.iter().max().unwrap());

        let mut distances = FxHashMap::default();
        for x in x_bounds.0..=x_bounds.1 {
            for y in y_bounds.0..=y_bounds.1 {
                let start = Point::new(x, y);
                let mut from_start = FxHashMap::default();
                for end in &points {
                    from_start.insert(end.clone(), start.manhattan_distance(end));
                }
                distances.insert(start, from_start);
            }
        }

        Self {
            x_bounds,
            y_bounds,
            distances,
        }
    }

    fn largest_finite(&self) -> usize {
        let mut regions: FxHashMap<Point, Vec<Point>> = FxHashMap::default();
        for point in self.distances.keys() {
            if let Some(closest) = self.get_closest(point) {
                if regions.contains_key(&closest) {
                    regions.get_mut(&closest).unwrap().push(point.clone());
                } else {
                    regions.insert(closest, vec![point.clone()]);
                }
            }
        }
        regions
            .values()
            .filter(|cluster| self.finite(cluster))
            .map(|cluster| cluster.len())
            .max()
            .unwrap()
    }

    fn get_closest(&self, point: &Point) -> Option<Point> {
        let distances = &self.distances[point];
        let min_distance: i64 = *distances.values().min().unwrap();
        let points: Vec<&Point> = distances
            .iter()
            .filter(|(_, &distance)| distance == min_distance)
            .map(|(point, _)| point)
            .collect();
        if points.len() == 1 {
            Some(points[0].clone())
        } else {
            None
        }
    }

    fn finite(&self, cluster: &Vec<Point>) -> bool {
        cluster.iter().all(|point| {
            self.x_bounds.0 != point.x
                && self.x_bounds.1 != point.x
                && self.y_bounds.0 != point.y
                && self.y_bounds.1 != point.y
        })
    }

    fn within_distance(&self, distance: i64) -> usize {
        // Assumes no points outside of min / max boundaries fall within the
        // max allowable distance, this assumption could be checked
        self.distances
            .values()
            .filter(|distances| distances.values().sum::<i64>() < distance)
            .count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points: Vec<Point> = Reader::default().read(|line| line.parse().unwrap());
    let point_grid = PointGrid::new(points);
    answer::part1(3251, point_grid.largest_finite());
    answer::part2(47841, point_grid.within_distance(10_000));
}
