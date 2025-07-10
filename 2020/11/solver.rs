use aoc::prelude::*;

#[derive(Debug, Clone, PartialEq)]
enum Seat {
    Occupied,
    Empty,
    Floor,
}

impl FromChar for Seat {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '#' => Some(Self::Occupied),
            'L' => Some(Self::Empty),
            '.' => Some(Self::Floor),
            _ => None,
        }
    }
}

#[derive(Debug)]
struct SeatingChart {
    chart: Grid<Seat>,
    look: bool,
}

impl SeatingChart {
    fn step(&mut self) -> bool {
        let mut changes: Vec<(Point, Seat)> = Vec::default();
        for (point, seat) in self.chart.iter() {
            let limit = match seat {
                Seat::Floor => None,
                Seat::Empty => Some(1),
                Seat::Occupied => Some(if self.look { 5 } else { 4 }),
            };
            let next_seat = match limit {
                None => Seat::Floor,
                Some(limit) => {
                    if self.neighbors(point) >= limit {
                        Seat::Empty
                    } else {
                        Seat::Occupied
                    }
                }
            };
            if seat != &next_seat {
                changes.push((point.clone(), next_seat));
            }
        }
        let changed = !changes.is_empty();
        for (point, seat) in changes {
            self.chart.add(point, seat);
        }
        changed
    }

    fn neighbors(&self, point: &Point) -> usize {
        Heading::values()
            .iter()
            .map(|heading| {
                let mut point = point.add(heading);
                if self.look {
                    while self.chart.is(&point, &Seat::Floor) {
                        point = point.add(heading);
                    }
                }
                point
            })
            .filter(|point| self.chart.is(point, &Seat::Occupied))
            .count()
    }

    fn occupied(&self) -> usize {
        self.chart.values(&Seat::Occupied).len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let chart = Reader::default().grid();
    answer::part1(2386, run(chart.clone(), false));
    answer::part2(2091, run(chart.clone(), true));
}

fn run(chart: Grid<Seat>, look: bool) -> usize {
    let mut chart = SeatingChart { chart, look };
    while chart.step() {}
    chart.occupied()
}
