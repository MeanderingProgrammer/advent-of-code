use aoc_lib::answer;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;

#[derive(Debug)]
enum Computation {
    Success(i64),
    Failure,
}

#[derive(Debug)]
struct Computer {
    registers: FxHashMap<String, i64>,
    instructions: Vec<String>,
    pointer: i64,
    num_outputs: i64,
}

impl Computer {
    fn new(initial_value: i64, instructions: Vec<String>) -> Self {
        Self {
            registers: [("a", initial_value), ("b", 0), ("c", 0), ("d", 0)]
                .into_iter()
                .map(|(reg, value)| (reg.to_string(), value))
                .collect(),
            instructions,
            pointer: 0,
            num_outputs: 0,
        }
    }

    fn run(&mut self) -> bool {
        let mut success = true;
        while self.has_instruction() && success && self.num_outputs < 100 {
            match self.run_next() {
                Computation::Success(adjustment) => self.pointer += adjustment,
                Computation::Failure => success = false,
            };
        }
        success
    }

    fn has_instruction(&self) -> bool {
        self.pointer >= 0 && self.pointer < (self.instructions.len() as i64)
    }

    fn run_next(&mut self) -> Computation {
        let instruction = &self.instructions[self.pointer as usize];
        let parts: Vec<&str> = instruction.split(' ').collect();
        match parts[0] {
            "cpy" => self.set(parts[2].to_string(), self.get(parts[1])),
            "inc" => self.set(parts[1].to_string(), self.get(parts[1]) + 1),
            "dec" => self.set(parts[1].to_string(), self.get(parts[1]) - 1),
            "jnz" => {
                if self.get(parts[1]) != 0 {
                    Computation::Success(self.get(parts[2]))
                } else {
                    Computation::Success(1)
                }
            }
            "out" => {
                if self.get(parts[1]) == self.num_outputs % 2 {
                    self.num_outputs += 1;
                    Computation::Success(1)
                } else {
                    Computation::Failure
                }
            }
            op => panic!("Unknown operation {op}"),
        }
    }

    fn get(&self, value: &str) -> i64 {
        match self.registers.get(value) {
            None => value.parse().unwrap(),
            Some(result) => *result,
        }
    }

    fn set(&mut self, register: String, value: i64) -> Computation {
        self.registers.insert(register, value);
        Computation::Success(1)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    answer::part1(198, run(lines));
}

fn run(lines: Vec<String>) -> i64 {
    let mut i = 0;
    loop {
        let mut computer = Computer::new(i, lines.clone());
        if computer.run() {
            return i;
        } else {
            i += 1;
        }
    }
}
