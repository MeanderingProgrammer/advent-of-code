use aoc_lib::answer;
use aoc_lib::collections::HashSet;
use aoc_lib::grid::Grid;
use aoc_lib::iter::Iter;
use aoc_lib::reader::Reader;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Point<const N: usize> {
    coords: [i32; N],
}

impl<const N: usize> Point<N> {
    fn new(x: i32, y: i32) -> Self {
        let mut coords = [0; N];
        assert!(N >= 2);
        coords[0] = x;
        coords[1] = y;
        Self { coords }
    }

    fn neighbors(&self) -> Vec<Self> {
        let mut result = vec![self.clone()];
        for i in 0..N {
            let mut next: Vec<Self> = Vec::default();
            for point in result {
                for delta in [-1, 0, 1] {
                    let mut point = point.clone();
                    point.coords[i] += delta;
                    next.push(point);
                }
            }
            result = next;
        }
        assert_eq!(self, &result.remove(result.len() / 2));
        result
    }
}

#[derive(Debug, Default)]
struct State<const N: usize> {
    active: HashSet<Point<N>>,
}

impl<const N: usize> State<N> {
    fn new(grid: &Grid<char>) -> Self {
        Self {
            active: grid
                .iter()
                .filter(|(_, value)| **value == '#')
                .map(|(point, _)| Point::new(point.x, point.y))
                .collect(),
        }
    }

    fn step(&self) -> Self {
        let counts = self
            .active
            .iter()
            .flat_map(|point| point.neighbors())
            .counts();
        let mut state = Self::default();
        for (point, count) in counts.into_iter() {
            let active = if self.active.contains(&point) {
                [2, 3].contains(&count)
            } else {
                count == 3
            };
            if active {
                state.active.insert(point);
            }
        }
        state
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Some);
    answer::part1(284, simulate::<3>(&grid));
    answer::part2(2240, simulate::<4>(&grid));
}

fn simulate<const N: usize>(grid: &Grid<char>) -> usize {
    let mut state: State<N> = State::new(grid);
    for _ in 0..6 {
        state = state.step();
    }
    state.active.len()
}
