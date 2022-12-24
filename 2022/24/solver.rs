use aoc_lib::answer;
use aoc_lib::grid::{Bound, Grid};
use aoc_lib::point::Point;
use aoc_lib::reader;
use std::collections::HashMap;

#[derive(Debug)]
enum Direction {
    Up,
    Right,
    Down, 
    Left,
}

type BlizzardGrid = Grid<char>;
type Blizzards = HashMap<Point, Direction>;

struct Valley {
    bounds: Bound,
    blizzards: Blizzards,
}

impl Valley {
    fn new(grid: BlizzardGrid) -> Self {
        let bounds = grid.bounds(0);
        let mut blizzards = Blizzards::new();
        grid.points().iter()
            .map(|point| (point, grid.get(point)))
            .filter(|(_, &value)| value != '.')
            .for_each(|(&point, value)| {
                let direction = match value {
                    '^' => Direction::Up,
                    '>' => Direction::Right,
                    'v' => Direction::Down,
                    '<' => Direction::Left,
                    _ => unreachable!(),
                };
                blizzards.insert(point.clone(), direction);
            });
        Self { bounds, blizzards }
    }

    fn start(&self) -> &Point {
        self.bounds.lower()
    }

    fn end(&self) -> &Point {
        self.bounds.upper()
    }

    fn next(&self) {
    }
}

fn main() {
    let mut valley = Valley::new(reader::read_grid(|ch| match ch {
        '<' | '^' | '>' | 'v' | '.' => Some(ch),
        _ => None,    
    }));
    println!("{:?}", valley.blizzards);
    println!("{:?}", valley.bounds);
    println!("{:?}", valley.start());
    println!("{:?}", valley.end());


    println!("");
    valley.next();
    println!("{:?}", valley.blizzards);

    //answer::part1(v1, s1);
    //answer::part2(v2, s2);
}
