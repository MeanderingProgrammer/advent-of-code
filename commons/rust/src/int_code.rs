#[derive(Debug)]
struct Parameter {
    value: i64,
    mode: u8,
}

impl Parameter {
    fn new(value: i64, mode: u8) -> Self {
        Self { value, mode }
    }

    fn get<T>(&self, computer: &Computer<T>) -> i64 {
        match self.mode {
            0 | 2 => computer.get(self.index(computer)),
            1 => self.value,
            _ => panic!("Unknown mode get: {0}", self.mode),
        }
    }

    fn index<T>(&self, computer: &Computer<T>) -> usize {
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

pub trait Bus {
    fn active(&self) -> bool;
    fn get_input(&mut self) -> i64;
    fn add_output(&mut self, value: i64);
}

#[derive(Debug, Default)]
pub struct NoopBus {}

impl Bus for NoopBus {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        0
    }

    fn add_output(&mut self, _: i64) {}
}

#[derive(Debug)]
pub struct Computer<T> {
    pub bus: T,
    memory: Vec<i64>,
    code: i64,
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
        let response = self.next();
        // Update pointer
        self.pointer = match response {
            Response::Jump(index) => index,
            _ => self.pointer + 1,
        };
        // Update base
        self.base += match response {
            Response::AdjustBase(amount) => amount,
            _ => 0,
        };
        // Interactions with bus / memory
        match response {
            Response::SetValue(index, value) => self.set(index, value),
            Response::Store(index) => {
                let value = self.bus.get_input();
                self.set(index, value);
            }
            Response::Load(value) => self.bus.add_output(value),
            _ => (),
        };
        // Whether or not to Halt
        !matches!(response, Response::Halt)
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
            pointer: 0,
            base: 0,
        }
    }

    fn next(&mut self) -> Response {
        self.code = self.memory[self.pointer];
        match self.code % 100 {
            1 => {
                let value = self.param(1).get(self) + self.param(2).get(self);
                Response::SetValue(self.param(3).index(self), value)
            }
            2 => {
                let value = self.param(1).get(self) * self.param(2).get(self);
                Response::SetValue(self.param(3).index(self), value)
            }
            3 => Response::Store(self.param(1).index(self)),
            4 => Response::Load(self.param(1).get(self)),
            5 => {
                let is_true = self.param(1).get(self) != 0;
                let p2 = self.param(2);
                if is_true {
                    Response::Jump(p2.get(self) as usize)
                } else {
                    Response::Noop
                }
            }
            6 => {
                let is_true = self.param(1).get(self) == 0;
                let p2 = self.param(2);
                if is_true {
                    Response::Jump(p2.get(self) as usize)
                } else {
                    Response::Noop
                }
            }
            7 => {
                let is_true = self.param(1).get(self) < self.param(2).get(self);
                Response::SetValue(self.param(3).index(self), if is_true { 1 } else { 0 })
            }
            8 => {
                let is_true = self.param(1).get(self) == self.param(2).get(self);
                Response::SetValue(self.param(3).index(self), if is_true { 1 } else { 0 })
            }
            9 => Response::AdjustBase(self.param(1).get(self) as usize),
            99 => Response::Halt,
            _ => panic!("Unknown code: {0}", self.code),
        }
    }

    fn param(&mut self, mode_offset: usize) -> Parameter {
        let mode = self
            .code
            .to_string()
            .chars()
            .rev()
            .nth(mode_offset + 1)
            .unwrap_or('0')
            .to_digit(10)
            .unwrap();
        self.pointer += 1;
        Parameter::new(self.memory[self.pointer], mode as u8)
    }

    pub fn get(&self, index: usize) -> i64 {
        if index < self.memory.len() {
            self.memory[index]
        } else {
            0
        }
    }

    fn set(&mut self, index: usize, value: i64) {
        if index >= self.memory.len() {
            self.memory.resize(index + 1, 0);
        }
        self.memory[index] = value;
    }
}
