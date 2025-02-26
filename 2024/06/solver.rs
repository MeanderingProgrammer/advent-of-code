use aoc::{Direction, FromChar, Grid, HashSet, Point, Reader, answer};
use rayon::prelude::*;

#[derive(Debug, Clone, PartialEq)]
enum Element {
    Start,
    Empty,
    Obstacle,
}

impl FromChar for Element {
    fn from_char(ch: char) -> Option<Self> {
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

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    point: Point,
    direction: Direction,
}

impl State {
    fn next(&self) -> Point {
        self.point.add(&self.direction)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let grid = Reader::default().grid();
    let start = grid.value(&Element::Start);
    let path = follow(&grid, &start, None).unwrap();
    answer::part1(5516, path.len());
    answer::part2(2008, obstacles(&grid, &start, path));
}

fn follow(grid: &Grid<Element>, start: &Point, obstacle: Option<&Point>) -> Option<HashSet<Point>> {
    let mut seen: HashSet<State> = HashSet::default();
    let mut state = State {
        point: start.clone(),
        direction: Direction::Up,
    };
    while grid.has(&state.point) {
        if seen.contains(&state) {
            return None;
        }
        seen.insert(state.clone());
        let next = state.next();
        if Some(&next) == obstacle || grid.is(&next, &Element::Obstacle) {
            state.direction = state.direction.right();
        } else {
            state.point = next;
        }
    }
    Some(if obstacle.is_none() {
        seen.into_iter().map(|state| state.point).collect()
    } else {
        HashSet::default()
    })
}

fn obstacles(grid: &Grid<Element>, start: &Point, options: HashSet<Point>) -> usize {
    options
        .into_par_iter()
        .filter(|point| match grid[point] {
            Element::Start => false,
            _ => follow(grid, start, Some(point)).is_none(),
        })
        .count()
}
