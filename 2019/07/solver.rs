use aoc::int_code::{Bus, Computer};
use aoc::{answer, Iter, Reader};
use std::collections::VecDeque;

#[derive(Debug)]
struct Amplifier {
    inputs: VecDeque<i64>,
    outputs: Vec<i64>,
    load: bool,
    pause: bool,
}

impl Amplifier {
    fn new(setting: i64, pause: bool) -> Self {
        Self {
            inputs: [setting].into(),
            outputs: Vec::default(),
            load: false,
            pause,
        }
    }
}

impl Bus for Amplifier {
    fn active(&self) -> bool {
        !self.pause || !self.load
    }

    fn get_input(&mut self) -> i64 {
        self.inputs.pop_front().unwrap()
    }

    fn add_output(&mut self, value: i64) {
        self.load = true;
        self.outputs.push(value);
    }
}

#[derive(Debug)]
struct AmplifierCpu {
    computer: Computer<Amplifier>,
}

impl AmplifierCpu {
    fn new(memory: &[i64], setting: i64, pause: bool) -> Self {
        let amplifier = Amplifier::new(setting, pause);
        let computer = Computer::new(amplifier, memory);
        Self { computer }
    }

    fn run(&mut self, input: i64) -> (bool, i64) {
        self.bus().load = false;
        self.bus().inputs.push_back(input);
        self.computer.run();
        (!self.bus().active(), *self.bus().outputs.last().unwrap())
    }

    fn bus(&mut self) -> &mut Amplifier {
        &mut self.computer.bus
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    answer::part1(38834, run(&memory, &[0, 1, 2, 3, 4], false));
    answer::part2(69113332, run(&memory, &[5, 6, 7, 8, 9], true));
}

fn run(memory: &[i64], sequence: &[i64], pause: bool) -> i64 {
    sequence
        .iter()
        .permutations()
        .map(|possibility| check(memory, possibility, pause))
        .max()
        .unwrap()
}

fn check(memory: &[i64], sequence: Vec<&i64>, pause: bool) -> i64 {
    let mut amplifiers: Vec<_> = sequence
        .into_iter()
        .map(|entry| AmplifierCpu::new(memory, *entry, pause))
        .collect();
    let (mut output, mut state) = (0, true);
    while state {
        for amplifier in amplifiers.iter_mut() {
            let (amp_state, amp_output) = amplifier.run(output);
            state &= amp_state;
            output = amp_output;
        }
    }
    output
}
