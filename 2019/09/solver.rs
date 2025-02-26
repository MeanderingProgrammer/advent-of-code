use aoc::int_code::{Bus, Computer};
use aoc::{Reader, answer};

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
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    answer::part1(3512778005, run(&memory, 1));
    answer::part2(35920, run(&memory, 2));
}

fn run(memory: &[i64], input: i64) -> i64 {
    let program = BoostProgram {
        input,
        output: None,
    };
    let mut computer = Computer::new(program, memory);
    computer.run();
    computer.bus.output.unwrap()
}
