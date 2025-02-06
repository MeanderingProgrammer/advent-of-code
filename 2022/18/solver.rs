use aoc::{answer, HashSet, Point3d, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
struct Bound {
    lower: Point3d,
    upper: Point3d,
}

impl Bound {
    fn contains(&self, point: &Point3d) -> bool {
        let contains_x = point.x >= self.lower.x && point.x <= self.upper.x;
        let contains_y = point.y >= self.lower.y && point.y <= self.upper.y;
        let contains_z = point.z >= self.lower.z && point.z <= self.upper.z;
        contains_x && contains_y && contains_z
    }
}

#[derive(Debug)]
struct Grid {
    points: HashSet<Point3d>,
}

impl Grid {
    fn missing(&self, point: &Point3d) -> bool {
        !self.points.contains(point)
    }

    fn fill(&self) -> HashSet<Point3d> {
        let mut seen = HashSet::default();
        let bound = self.get_bound();
        let mut q = VecDeque::default();
        q.push_back(bound.lower.clone());
        while !q.is_empty() {
            let point = q.pop_front().unwrap();
            for neighbor in point.neighbors() {
                if !seen.contains(&neighbor) && self.missing(&neighbor) && bound.contains(&neighbor)
                {
                    q.push_back(neighbor.clone());
                    seen.insert(neighbor.clone());
                }
            }
        }
        seen
    }

    fn get_bound(&self) -> Bound {
        fn get_min(values: &[i32]) -> i32 {
            values.iter().min().unwrap() - 1
        }
        fn get_max(values: &[i32]) -> i32 {
            values.iter().max().unwrap() + 1
        }
        let xs: Vec<i32> = self.points.iter().map(|point| point.x).collect();
        let ys: Vec<i32> = self.points.iter().map(|point| point.y).collect();
        let zs: Vec<i32> = self.points.iter().map(|point| point.z).collect();
        Bound {
            lower: Point3d::new(get_min(&xs), get_min(&ys), get_min(&zs)),
            upper: Point3d::new(get_max(&xs), get_max(&ys), get_max(&zs)),
        }
    }

    fn surface_area(&self, f: impl Fn(&Point3d) -> bool) -> usize {
        self.points
            .iter()
            .map(|point| {
                let neighbors = point.neighbors().into_iter();
                neighbors.filter(|neighbor| f(neighbor)).count()
            })
            .sum()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points: Vec<Point3d> = Reader::default().lines();
    let grid = Grid {
        points: points.into_iter().collect(),
    };
    let boundary = grid.fill();
    answer::part1(4288, grid.surface_area(|point| grid.missing(point)));
    answer::part2(2494, grid.surface_area(|point| boundary.contains(point)));
}
