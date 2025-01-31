use aoc_lib::answer;
use aoc_lib::collections::HashMap;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::reader::Reader;

#[derive(Debug)]
struct Beam {
    x: i64,
    y: i64,
    called: bool,
    value: Option<i64>,
}

impl Beam {
    fn new(x: i64, y: i64) -> Self {
        Self {
            x,
            y,
            called: false,
            value: None,
        }
    }
}

impl Bus for Beam {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        let value = if !self.called { self.x } else { self.y };
        self.called = !self.called;
        value
    }

    fn add_output(&mut self, value: i64) {
        self.value = Some(value);
    }
}

#[derive(Debug)]
struct Tester {
    memory: Vec<i64>,
    beam_starts: HashMap<i64, i64>,
}

impl Tester {
    fn test(&self, x: i64, y: i64) -> i64 {
        let mut computer = Computer::new(Beam::new(x, y), &self.memory);
        computer.run();
        computer.bus.value.unwrap()
    }

    fn can_bound(&mut self, y: i64, offset: i64) -> bool {
        let x = self.left_most(y);
        self.test(x + offset, y - offset) == 1
    }

    fn left_most(&mut self, y: i64) -> i64 {
        let mut x = *self.beam_starts.get(&(y - 1)).unwrap_or(&0);
        while self.test(x, y) != 1 {
            x += 1;
        }
        self.beam_starts.insert(y, x);
        x
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().read_csv();
    let mut tester = Tester {
        memory,
        beam_starts: HashMap::default(),
    };
    answer::part1(160, affected_points(&mut tester, 50));
    answer::part2(9441282, bounding_point(&mut tester, 100));
}

fn affected_points(tester: &mut Tester, size: i64) -> i64 {
    let mut affected = Vec::new();
    for y in 0..size {
        for x in 0..size {
            affected.push(tester.test(x, y));
        }
    }
    affected.iter().sum()
}

fn bounding_point(tester: &mut Tester, size: i64) -> i64 {
    let mut row = size;
    while !tester.can_bound(row, size - 1) {
        row += 1;
    }
    let x = tester.left_most(row);
    10_000 * x + (row - (size - 1))
}
