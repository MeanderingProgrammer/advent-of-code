use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashMap;

type Point = (i16, i16);

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
    chart: HashMap<Point, Seat>,
    look: bool,
}

impl SeatingChart {
    fn next(&self) -> Self {
        let mut next_chart = HashMap::new();
        self.chart.iter().for_each(|(p, seat)| {
            next_chart.insert(p.clone(), self.next_seat(p, seat));
        });
        Self {
            chart: next_chart,
            look: self.look,
        }
    }

    fn next_seat(&self, p: &Point, seat: &Seat) -> Seat {
        match seat {
            Seat::Floor => seat.clone(),
            Seat::Empty => {
                if self.adjacent_occupied(p) == 0 {
                    Seat::Occupied
                } else {
                    seat.clone()
                }
            }
            Seat::Occupied => {
                let to_empty = if self.look { 5 } else { 4 };
                if self.adjacent_occupied(p) >= to_empty {
                    Seat::Empty
                } else {
                    seat.clone()
                }
            }
        }
    }

    fn adjacent_occupied(&self, p: &Point) -> usize {
        let directions: Vec<Point> = vec![
            (1, 1),
            (1, 0),
            (1, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, 1),
            (0, -1),
        ];
        directions
            .into_iter()
            .map(|direction| self.explore_direction(p, direction))
            .filter(|&seat| seat == Some(&Seat::Occupied))
            .count()
    }

    fn explore_direction(&self, p: &Point, direction: Point) -> Option<&Seat> {
        let mut point = (p.0 + direction.0, p.1 + direction.1);
        let mut seat = self.chart.get(&point);
        if !self.look {
            seat
        } else {
            while seat == Some(&Seat::Floor) {
                point = (point.0 + direction.0, point.1 + direction.1);
                seat = self.chart.get(&point);
            }
            seat
        }
    }

    fn occupied(&self) -> usize {
        self.chart
            .values()
            .filter(|&seat| *seat == Seat::Occupied)
            .count()
    }
}

fn main() {
    answer::part1(2386, run_until_stable(false));
    answer::part2(2091, run_until_stable(true));
}

fn run_until_stable(look: bool) -> usize {
    let mut previous = SeatingChart {
        chart: HashMap::new(),
        look,
    };
    let mut current = SeatingChart {
        chart: get_chart(),
        look,
    };
    while previous != current {
        previous = current.clone();
        current = current.next();
    }
    previous.occupied()
}

fn get_chart() -> HashMap<Point, Seat> {
    let mut chart: HashMap<Point, Seat> = HashMap::new();
    reader::read_grid(|ch| Seat::from_ch(ch))
        .get_grid()
        .into_iter()
        .for_each(|(point, seat)| {
            chart.insert((point.x() as i16, point.y() as i16), seat);
        });
    chart
}
