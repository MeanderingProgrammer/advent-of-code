use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;

#[derive(Debug, Clone, PartialEq)]
enum Element {
    Start,
    Empty,
    Obstacle,
}

impl Element {
    fn from_ch(ch: char) -> Option<Self> {
        if ch == '^' {
            Some(Self::Start)
        } else if ch == '.' {
            Some(Self::Empty)
        } else if ch == '#' {
            Some(Self::Obstacle)
        } else {
            None
        }
    }
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct State {
    point: Point,
    direction: Direction,
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().read_grid(Element::from_ch);
    let start: Point = grid
        .points()
        .into_iter()
        .find(|point| grid.get(point) == &Element::Start)
        .unwrap()
        .clone();
    let path = follow(&grid, &start).unwrap();
    answer::part1(5516, path.len());
    answer::part2(2008, obstacles(grid, &start, path));
}

fn follow(grid: &Grid<Element>, start: &Point) -> Option<FxHashSet<Point>> {
    let mut seen: FxHashSet<State> = FxHashSet::default();
    let mut point: Point = start.clone();
    let mut direction = Direction::Up;
    while grid.contains(&point) {
        let state = State {
            point: point.clone(),
            direction: direction.clone(),
        };
        if seen.contains(&state) {
            return None;
        }
        seen.insert(state);
        let next_point = &point + &direction;
        if grid.get_or(&next_point).unwrap_or(&Element::Empty) == &Element::Obstacle {
            direction = direction.right();
        } else {
            point = next_point;
        }
    }
    Some(seen.into_iter().map(|state| state.point).collect())
}

fn obstacles(mut grid: Grid<Element>, start: &Point, options: FxHashSet<Point>) -> usize {
    let mut result = 0;
    for point in options.iter() {
        if grid.get_or(point).unwrap_or(&Element::Obstacle) != &Element::Start {
            grid.add(point.clone(), Element::Obstacle);
            if follow(&grid, start).is_none() {
                result += 1;
            }
            grid.add(point.clone(), Element::Empty);
        }
    }
    result
}
