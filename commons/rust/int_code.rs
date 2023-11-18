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
            0 | 2 => computer.get(self.index(computer)),
            1 => self.value,
            _ => panic!("Unknown mode get: {0}", self.mode),
        }
    }

    fn index<T: Bus + Debug>(&self, computer: &Computer<T>) -> usize {
        match self.mode {
            0 => self.value as usize,
            2 => computer.base + (self.value as usize),
            _ => panic!("Unknown mode index: {0}", self.mode),
        }
    }
}

#[derive(Debug)]
enum Response {
    SetValue(usize, i64),
    Halt,
    Store(usize),
    Load(i64),
    Jump(usize),
    Noop,
    AdjustBase(usize),
}

trait Instruction<T>: Debug {
    fn process(&self, computer: &Computer<T>) -> Response;
    fn len(&self) -> usize;
}

#[derive(Debug)]
struct Math {
    f: fn(i64, i64) -> i64,
    v1: Parameter,
    v2: Parameter,
    v3: Parameter,
}

impl Math {
    fn new(f: fn(i64, i64) -> i64, v1: Parameter, v2: Parameter, v3: Parameter) -> Self {
        Self { f, v1, v2, v3 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Math {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::SetValue(
            self.v3.index(computer),
            (self.f)(self.v1.get(computer), self.v2.get(computer)),
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

impl<T: Bus + Debug> Instruction<T> for Halt {
    fn process(&self, _: &Computer<T>) -> Response {
        Response::Halt
    }

    fn len(&self) -> usize {
        0
    }
}

#[derive(Debug)]
struct Store {
    v1: Parameter,
}

impl Store {
    fn new(v1: Parameter) -> Self {
        Self { v1 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Store {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::Store(self.v1.index(computer))
    }

    fn len(&self) -> usize {
        1
    }
}

#[derive(Debug)]
struct Load {
    v1: Parameter,
}

impl Load {
    fn new(v1: Parameter) -> Self {
        Self { v1 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Load {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::Load(self.v1.get(computer))
    }

    fn len(&self) -> usize {
        1
    }
}

#[derive(Debug)]
struct JumpIf {
    f: fn(i64) -> bool,
    v1: Parameter,
    v2: Parameter,
}

impl JumpIf {
    fn new(f: fn(i64) -> bool, v1: Parameter, v2: Parameter) -> Self {
        Self { f, v1, v2 }
    }
}

impl<T: Bus + Debug> Instruction<T> for JumpIf {
    fn process(&self, computer: &Computer<T>) -> Response {
        if (self.f)(self.v1.get(computer)) {
            Response::Jump(self.v2.get(computer) as usize)
        } else {
            Response::Noop
        }
    }

    fn len(&self) -> usize {
        2
    }
}

#[derive(Debug)]
struct Comparison {
    f: fn(i64, i64) -> bool,
    v1: Parameter,
    v2: Parameter,
    v3: Parameter,
}

impl Comparison {
    fn new(f: fn(i64, i64) -> bool, v1: Parameter, v2: Parameter, v3: Parameter) -> Self {
        Self { f, v1, v2, v3 }
    }
}

impl<T: Bus + Debug> Instruction<T> for Comparison {
    fn process(&self, computer: &Computer<T>) -> Response {
        let is_true = (self.f)(self.v1.get(computer), self.v2.get(computer));
        Response::SetValue(self.v3.index(computer), if is_true { 1 } else { 0 })
    }

    fn len(&self) -> usize {
        3
    }
}

#[derive(Debug)]
struct BaseAdjuster {
    v1: Parameter,
}

impl BaseAdjuster {
    fn new(v1: Parameter) -> Self {
        Self { v1 }
    }
}

impl<T: Bus + Debug> Instruction<T> for BaseAdjuster {
    fn process(&self, computer: &Computer<T>) -> Response {
        Response::AdjustBase(self.v1.get(computer) as usize)
    }

    fn len(&self) -> usize {
        1
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
        if index < self.memory.len() {
            self.memory[index]
        } else {
            0
        }
    }

    pub fn run(&mut self) {
        while self.bus.active() && self.run_next() {}
    }

    fn run_next(&mut self) -> bool {
        let instruction = self.next();
        let response = instruction.process(self);
        match response {
            Response::SetValue(index, value) => {
                self.set(index, value);
                self.pointer += 1 + instruction.len();
                true
            }
            Response::Halt => false,
            Response::Store(index) => {
                self.set(index, self.bus.get_input());
                self.pointer += 1 + instruction.len();
                true
            }
            Response::Load(value) => {
                self.bus.add_output(value);
                self.pointer += 1 + instruction.len();
                true
            }
            Response::Jump(index) => {
                self.pointer = index;
                true
            }
            Response::Noop => {
                self.pointer += 1 + instruction.len();
                true
            }
            Response::AdjustBase(amount) => {
                self.base += amount;
                self.pointer += 1 + instruction.len();
                true
            }
        }
    }

    fn next(&self) -> Box<dyn Instruction<T>> {
        let opcode = self.memory[self.pointer] % 100;
        match opcode {
            1 => Box::new(Math::new(
                |v1, v2| v1 + v2,
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            2 => Box::new(Math::new(
                |v1, v2| v1 * v2,
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            3 => Box::new(Store::new(self.parameter(1))),
            4 => Box::new(Load::new(self.parameter(1))),
            5 => Box::new(JumpIf::new(
                |value| value != 0,
                self.parameter(1),
                self.parameter(2),
            )),
            6 => Box::new(JumpIf::new(
                |value| value == 0,
                self.parameter(1),
                self.parameter(2),
            )),
            7 => Box::new(Comparison::new(
                |v1, v2| v1 < v2,
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            8 => Box::new(Comparison::new(
                |v1, v2| v1 == v2,
                self.parameter(1),
                self.parameter(2),
                self.parameter(3),
            )),
            9 => Box::new(BaseAdjuster::new(self.parameter(1))),
            99 => Box::new(Halt::new()),
            _ => panic!("Unknown opcode: {opcode}"),
        }
    }

    fn parameter(&self, i: usize) -> Parameter {
        let code = self.memory[self.pointer];
        let mode_char = code.to_string().chars().rev().nth(i + 1).unwrap_or('0');
        let mode = mode_char.to_digit(10).unwrap() as u8;
        Parameter::new(self.memory[self.pointer + i], mode)
    }

    fn set(&mut self, index: usize, value: i64) {
        if index >= self.memory.len() {
            self.memory.resize(index + 1, 0);
        }
        self.memory[index] = value;
    }
}
