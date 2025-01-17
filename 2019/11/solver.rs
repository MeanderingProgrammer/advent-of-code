use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use std::collections::HashMap;

#[derive(Debug)]
struct PaintBot {
    direction: Direction,
    position: Point,
    grid: HashMap<Point, i64>,
    color: bool,
}

impl PaintBot {
    fn new(setting: i64) -> Self {
        Self {
            direction: Direction::Up,
            position: Point::default(),
            grid: [(Point::default(), setting)].into(),
            color: true,
        }
    }

    fn grid_str(&self) -> String {
        let mut grid: Grid<char> = Grid::default();
        self.grid
            .iter()
            .filter(|(_, &value)| value == 1)
            .for_each(|(position, _)| grid.add(position.clone(), '#'));
        grid.to_string()
    }
}

impl Bus for PaintBot {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        *self.grid.get(&self.position).unwrap_or(&0)
    }

    fn add_output(&mut self, value: i64) {
        if self.color {
            self.grid.insert(self.position.clone(), value);
        } else {
            self.direction = match value {
                0 => self.direction.left(),
                1 => self.direction.right(),
                _ => panic!("Unhandled input: {value}"),
            };
            self.position = self.position.add(&self.direction);
        }
        self.color = !self.color;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().read_csv();
    answer::part1(1909, run(&memory, 0).grid.len());
    let expected = [
        "..##.#..#.####.####.#..#.#..#.###..#..#",
        "...#.#..#.#....#....#.#..#..#.#..#.#..#",
        "...#.#..#.###..###..##...####.#..#.####",
        "...#.#..#.#....#....#.#..#..#.###..#..#",
        "#..#.#..#.#....#....#.#..#..#.#....#..#",
        ".##...##..#....####.#..#.#..#.#....#..#",
    ];
    answer::part2(
        "\n".to_owned() + &expected.join("\n"),
        "\n".to_owned() + &run(&memory, 1).grid_str(),
    );
}

fn run(memory: &[i64], settting: i64) -> PaintBot {
    let mut computer = Computer::new(PaintBot::new(settting), memory);
    computer.run();
    computer.bus
}
