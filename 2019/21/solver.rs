use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::reader::Reader;
use std::collections::VecDeque;

#[derive(Debug)]
struct JumpDroid {
    program: VecDeque<char>,
    value: Option<i64>,
}

impl JumpDroid {
    fn new(actions: Vec<&str>) -> Self {
        let mut program: Vec<char> = Vec::default();
        actions.into_iter().for_each(|action| {
            program.append(&mut action.chars().collect());
            program.push('\n');
        });
        Self {
            program: program.into(),
            value: None,
        }
    }
}

impl Bus for JumpDroid {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        self.program.pop_front().unwrap() as i64
    }

    fn add_output(&mut self, value: i64) {
        self.value = Some(value);
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().read_csv();
    answer::part1(
        19357761,
        run_droid(
            &memory,
            vec![
                "NOT A J", // If one ahead is missing always Jump
                "NOT C T", "OR T J", // If 3 ahead is missing
                "NOT B T", "OR T J",  // If 2 ahead is missing
                "AND D J", // Must always have thing 4 tiles ahead
                "NOT A T", "AND A T", // Force T to False
                "WALK",    // Start the script
            ],
        ),
    );
    answer::part2(
        1142249706,
        run_droid(
            &memory,
            vec![
                "NOT A J", // If one ahead is missing always Jump
                "NOT C T", "OR T J", // If 3 ahead is missing
                "NOT B T", "OR T J",  // If 2 ahead is missing
                "AND D J", // Must always have thing 4 tiles ahead
                "NOT A T", "AND A T", // Force T to False
                "OR E T", "OR H T", "AND T J", // If after we land is blank
                "RUN",     // Start the script
            ],
        ),
    );
}

fn run_droid(memory: &[i64], actions: Vec<&str>) -> i64 {
    let mut computer = Computer::new(JumpDroid::new(actions), memory);
    computer.run();
    computer.bus.value.unwrap()
}
