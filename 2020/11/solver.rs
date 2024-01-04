use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Heading, Point};
use aoc_lib::reader;
use strum::IntoEnumIterator;

#[derive(Debug, Clone, PartialEq)]
enum Seat {
    Occupied,
    Empty,
    Floor,
}

impl ToString for Seat {
    fn to_string(&self) -> String {
        match self {
            Self::Occupied => "#".to_string(),
            Self::Empty => "L".to_string(),
            Self::Floor => ".".to_string(),
        }
    }
}

impl Seat {
    fn from_ch(ch: char) -> Option<Self> {
        match ch {
            '#' => Some(Self::Occupied),
            'L' => Some(Self::Empty),
            '.' => Some(Self::Floor),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
struct SeatingChart {
    chart: Grid<Seat>,
    look: bool,
}

impl SeatingChart {
    fn next(&self) -> Self {
        let mut next_chart = Grid::new();
        self.chart.points().into_iter().for_each(|p| {
            next_chart.add(p.clone(), self.next_seat(p));
        });
        Self {
            chart: next_chart,
            look: self.look,
        }
    }

    fn next_seat(&self, p: &Point) -> Seat {
        match self.chart.get(p) {
            Seat::Floor => Seat::Floor,
            Seat::Empty => {
                if self.adjacent_occupied(p) == 0 {
                    Seat::Occupied
                } else {
                    Seat::Empty
                }
            }
            Seat::Occupied => {
                let to_empty = if self.look { 5 } else { 4 };
                if self.adjacent_occupied(p) >= to_empty {
                    Seat::Empty
                } else {
                    Seat::Occupied
                }
            }
        }
    }

    fn adjacent_occupied(&self, p: &Point) -> usize {
        Heading::iter()
            .map(|heading| self.explore_direction(p, &heading))
            .filter(|&seat| seat == Some(&Seat::Occupied))
            .count()
    }

    fn explore_direction(&self, p: &Point, heading: &Heading) -> Option<&Seat> {
        let mut point = p + heading;
        let mut seat = self.chart.get_or(&point);
        if !self.look {
            seat
        } else {
            while seat == Some(&Seat::Floor) {
                point = &point + heading;
                seat = self.chart.get_or(&point);
            }
            seat
        }
    }

    fn occupied(&self) -> usize {
        self.chart
            .values()
            .into_iter()
            .filter(|&seat| *seat == Seat::Occupied)
            .count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    answer::part1(2386, run_until_stable(false));
    answer::part2(2091, run_until_stable(true));
}

fn run_until_stable(look: bool) -> usize {
    let mut previous = SeatingChart {
        chart: Grid::new(),
        look,
    };
    let mut current = SeatingChart {
        chart: reader::read_grid(|ch| Seat::from_ch(ch)),
        look,
    };
    while previous != current {
        previous = current.clone();
        current = current.next();
    }
    previous.occupied()
}
