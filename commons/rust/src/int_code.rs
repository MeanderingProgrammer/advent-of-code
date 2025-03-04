#[derive(Debug)]
enum Mode {
    Position,
    Immediate,
    Relative,
}

impl From<i64> for Mode {
    fn from(value: i64) -> Self {
        match value {
            0 => Self::Position,
            1 => Self::Immediate,
            2 => Self::Relative,
            mode => panic!("Unknown mode: {mode}"),
        }
    }
}

#[derive(Debug)]
enum Method {
    Get,
    Idx,
}

#[derive(Debug)]
enum Response {
    Set(i64),
    Store(i64),
    Load(i64),
    Jump(i64),
    Noop,
    Base(i64),
    Halt,
}

pub trait Bus {
    fn active(&self) -> bool;
    fn get_input(&mut self) -> i64;
    fn add_output(&mut self, value: i64);
}

#[derive(Debug)]
pub struct Computer<T> {
    pub bus: T,
    memory: Vec<i64>,
    code: i64,
    parameter: usize,
    pointer: usize,
    base: usize,
}

impl<T> Computer<T>
where
    T: Bus,
{
    pub fn run(&mut self) {
        while self.bus.active() && self.run_next() {}
    }

    fn run_next(&mut self) -> bool {
        let mut increment = true;
        let mut done = false;
        match self.step() {
            Response::Set(value) => {
                let index = self.next(Method::Idx);
                self.set(index, value);
            }
            Response::Store(index) => {
                let value = self.bus.get_input();
                self.set(index, value);
            }
            Response::Load(value) => {
                self.bus.add_output(value);
            }
            Response::Jump(index) => {
                increment = false;
                self.pointer = index as usize;
            }
            Response::Noop => {}
            Response::Base(amount) => {
                self.base += amount as usize;
            }
            Response::Halt => done = true,
        };
        self.pointer += if increment { 1 } else { 0 };
        !done
    }
}

impl<T> Computer<T>
where
    T: Default,
{
    pub fn default(memory: &[i64]) -> Self {
        Self::new(T::default(), memory)
    }
}

impl<T> Computer<T> {
    pub fn new(bus: T, memory: &[i64]) -> Self {
        Self {
            bus,
            memory: memory.to_vec(),
            code: 0,
            parameter: 0,
            pointer: 0,
            base: 0,
        }
    }

    fn step(&mut self) -> Response {
        self.code = self.memory[self.pointer];
        self.parameter = 0;
        match self.code % 100 {
            // Day 2: add
            1 => Response::Set(self.next(Method::Get) + self.next(Method::Get)),
            // Day 2: multiply
            2 => Response::Set(self.next(Method::Get) * self.next(Method::Get)),
            // Day 5: input
            3 => Response::Store(self.next(Method::Idx)),
            // Day 5: output
            4 => Response::Load(self.next(Method::Get)),
            // Day 5: jump if true
            5 => {
                let (v1, v2) = (self.next(Method::Get), self.next(Method::Get));
                if v1 != 0 {
                    Response::Jump(v2)
                } else {
                    Response::Noop
                }
            }
            // Day 5: jump if false
            6 => {
                let (v1, v2) = (self.next(Method::Get), self.next(Method::Get));
                if v1 == 0 {
                    Response::Jump(v2)
                } else {
                    Response::Noop
                }
            }
            // Day 5: less than
            7 => {
                let (v1, v2) = (self.next(Method::Get), self.next(Method::Get));
                Response::Set(if v1 < v2 { 1 } else { 0 })
            }
            // Day 5: equal
            8 => {
                let (v1, v2) = (self.next(Method::Get), self.next(Method::Get));
                Response::Set(if v1 == v2 { 1 } else { 0 })
            }
            // Day 9: adjust relative base
            9 => Response::Base(self.next(Method::Get)),
            // Day 2: halt
            99 => Response::Halt,
            code => panic!("Unknown code: {code}"),
        }
    }

    fn next(&mut self, method: Method) -> i64 {
        self.parameter += 1;
        let n = 10i64.pow((self.parameter + 1) as u32);
        let mode = (self.code / n % 10).into();
        self.pointer += 1;
        let value = self.memory[self.pointer];
        match method {
            Method::Idx => self.index(&mode, value),
            Method::Get => match mode {
                Mode::Position | Mode::Relative => {
                    let index = self.index(&mode, value);
                    self.get(index as usize)
                }
                Mode::Immediate => value,
            },
        }
    }

    fn index(&self, mode: &Mode, value: i64) -> i64 {
        let offset = match mode {
            Mode::Position => 0,
            Mode::Relative => self.base as i64,
            Mode::Immediate => panic!("Immediate mode does not support indexing"),
        };
        offset + value
    }

    pub fn get(&self, index: usize) -> i64 {
        if index < self.memory.len() {
            self.memory[index]
        } else {
            0
        }
    }

    fn set(&mut self, index: i64, value: i64) {
        let index = index as usize;
        if index >= self.memory.len() {
            self.memory.resize(index + 1, 0);
        }
        self.memory[index] = value;
    }
}
