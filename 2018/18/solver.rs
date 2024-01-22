use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader::Reader;
use std::collections::HashMap;

#[derive(Debug, Default, PartialEq)]
enum State {
    #[default]
    Open,
    Tree,
    Yard,
}

impl ToString for State {
    fn to_string(&self) -> String {
        match self {
            Self::Open => ".".to_string(),
            Self::Tree => "|".to_string(),
            Self::Yard => "#".to_string(),
        }
    }
}
impl State {
    fn from_ch(ch: char) -> Option<Self> {
        match ch {
            '.' => Some(Self::Open),
            '|' => Some(Self::Tree),
            '#' => Some(Self::Yard),
            _ => None,
        }
    }
}

#[derive(Debug)]
struct Landscape {
    grid: Grid<State>,
}

impl Landscape {
    fn step(&mut self) {
        let mut updates: HashMap<Point, State> = HashMap::new();
        for point in self.grid.points() {
            match self.grid.get(point) {
                State::Open => {
                    if self.count(point, State::Tree) >= 3 {
                        updates.insert(point.clone(), State::Tree);
                    }
                }
                State::Tree => {
                    if self.count(point, State::Yard) >= 3 {
                        updates.insert(point.clone(), State::Yard);
                    }
                }
                State::Yard => {
                    if self.count(point, State::Yard) == 0 || self.count(point, State::Tree) == 0 {
                        updates.insert(point.clone(), State::Open);
                    }
                }
            }
        }
        for (point, value) in updates {
            self.grid.add(point, value);
        }
    }

    fn count(&self, point: &Point, state: State) -> usize {
        point
            .diagonal_neighbors()
            .iter()
            .filter(|neighbor| self.grid.contains(neighbor) && self.grid.get(neighbor) == &state)
            .count()
    }

    fn resource_value(&self) -> usize {
        self.resource_count(State::Tree) * self.resource_count(State::Yard)
    }

    fn resource_count(&self, state: State) -> usize {
        self.grid.points_with_value(state).len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    answer::part1(515496, run(10));
    answer::part2(233058, run(1_000_000_000));
}

fn run(n: usize) -> usize {
    let mut landscape = Landscape {
        grid: Reader::default().read_grid(State::from_ch),
    };
    let mut scores = vec![landscape.resource_value()];
    for _ in 0..n {
        landscape.step();
        scores.push(landscape.resource_value());
        if let Some(result) =
            find_pattern(&scores).map(|(start, pattern)| pattern[(n - start) % pattern.len()])
        {
            return result;
        }
    }
    *scores.last().unwrap()
}

fn find_pattern(values: &[usize]) -> Option<(usize, &[usize])> {
    for i in 1..values.len() - 1 {
        if values[i - 1..=i] == values[values.len() - 2..=values.len() - 1] {
            return Some((i - 1, &values[i - 1..values.len() - 2]));
        }
    }
    None
}
