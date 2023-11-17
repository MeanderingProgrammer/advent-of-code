use std::fmt::Debug;

#[derive(Debug)]
struct Parameter {
    value: i64,
    mode: u8,
}

impl Parameter {
    fn new(value: i64, mode: u8) -> Self {
        Self { value, mode }
    }

    fn get<T: Bus + Debug>(&self, computer: &Computer<T>) -> i64 {
        match self.mode {
            0 => computer.get(self.index(computer)),
            _ => panic!("Unknown mode get: {0}", self.mode),
        }
    }

    fn index<T: Bus + Debug>(&self, computer: &Computer<T>) -> usize {
        match self.mode {
            0 => self.value as usize,
            _ => panic!("Unknown mode index: {0}", self.mode),
        }
    }
}

#[derive(Debug)]
enum Response {
    SetValue(usize, i64),
    Halt,
}

trait Instruction<T>: Debug {
    fn process(&self, computer: &Computer<T>) -> Response;
    fn len(&self) -> usize;
}

#[derive(Debug)]
struct Addition {
    v1: Parameter,
    v2: Parameter,
    v3: Parameter,
}

impl Addition {
    fn new(v1: Parameter, v2: Parameter, v3: Parameter) -> Self {
        Self { v1, v2, v3 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Addition {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::SetValue(
            self.v3.index(computer),
            self.v1.get(computer) + self.v2.get(computer),
        )
    }

    fn len(&self) -> usize {
        3
    }
}

#[derive(Debug)]
struct Multiplication {
    v1: Parameter,
    v2: Parameter,
    v3: Parameter,
}

impl Multiplication {
    fn new(v1: Parameter, v2: Parameter, v3: Parameter) -> Self {
        Self { v1, v2, v3 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Multiplication {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::SetValue(
            self.v3.index(computer),
            self.v1.get(computer) * self.v2.get(computer),
        )
    }

    fn len(&self) -> usize {
        3
    }
}

#[derive(Debug)]
struct Halt {}

impl Halt {
    fn new() -> Self {
        Self {}
    }
}

impl<T> Instruction<T> for Halt {
    fn process(&self, _: &Computer<T>) -> Response {
        Response::Halt
    }

    fn len(&self) -> usize {
        0
    }
}

pub trait Bus {
    fn active(&self) -> bool;
    fn get_input(&self) -> i64;
    fn add_output(&mut self, value: i64);
}

#[derive(Debug)]
pub struct NoopBus {}

impl NoopBus {
    pub fn new() -> Self {
        Self {}
    }
}

impl Bus for NoopBus {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&self) -> i64 {
        0
    }

    fn add_output(&mut self, _: i64) {}
}

#[derive(Debug)]
pub struct Computer<T> {
    pub bus: T,
    memory: Vec<i64>,
    pointer: usize,
    base: usize,
}

impl<T: Bus + Debug> Computer<T> {
    pub fn new(bus: T, memory: Vec<i64>) -> Self {
        Self {
            bus,
            memory,
            pointer: 0,
            base: 0,
        }
    }

    pub fn get(&self, index: usize) -> i64 {
        self.memory[index]
    }

    pub fn run(&mut self) {
        while self.bus.active() && self.run_next() {}
    }

    fn run_next(&mut self) -> bool {
        let instruction = self.next();
        let response = instruction.process(self);
        match response {
            Response::SetValue(index, value) => {
                self.memory[index] = value;
                self.pointer += 1 + instruction.len();
                true
            }
            Response::Halt => false,
        }
    }

    fn next(&self) -> Box<dyn Instruction<T>> {
        let opcode = self.memory[self.pointer] % 100;
        match opcode {
            1 => Box::new(Addition::new(
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            2 => Box::new(Multiplication::new(
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            99 => Box::new(Halt::new()),
            _ => panic!("Unknown opcode: {opcode}"),
        }
    }

    fn parameter(&self, i: usize) -> Parameter {
        let code = self.memory[self.pointer];
        let mode_char = code.to_string().chars().nth(i + 2).unwrap_or('0');
        let mode = mode_char.to_digit(10).unwrap() as u8;
        Parameter::new(self.memory[self.pointer + i], mode)
    }
}
