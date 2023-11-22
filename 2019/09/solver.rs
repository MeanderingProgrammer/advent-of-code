use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::reader;

#[derive(Debug)]
struct BoostProgram {
    input: i64,
    output: Option<i64>,
}

impl Bus for BoostProgram {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        self.input
    }

    fn add_output(&mut self, value: i64) {
        self.output = Some(value);
    }
}

fn main() {
    answer::part1(3512778005, run(1));
    answer::part2(35920, run(2));
}

fn run(setting: i64) -> i64 {
    let mut computer = Computer::new(
        BoostProgram {
            input: setting,
            output: None,
        },
        reader::read_csv(),
    );
    computer.run();
    computer.bus.output.unwrap()
}
