use aoc::{answer, Convert, HashMap, HashSet, Iter, Parser, Reader};
use std::str::FromStr;

#[derive(Debug)]
struct Behavior {
    write: bool,
    direction: i16,
    next: u8,
}

impl FromStr for Behavior {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        //    - Write the value 1.
        //    - Move one slot to the right.
        //    - Continue with state B.
        let [write, direction, state] = s.lines().array().unwrap();
        let write = match last_word(write) {
            "0" => Ok(false),
            "1" => Ok(true),
            _ => Err(String::from("unhandled write")),
        };
        let direction = match last_word(direction) {
            "left" => Ok(-1),
            "right" => Ok(1),
            _ => Err(String::from("unhandled direction")),
        };
        Ok(Self {
            write: write?,
            direction: direction?,
            next: to_state(state),
        })
    }
}

#[derive(Debug)]
struct Rule {
    zero: Behavior,
    one: Behavior,
}

impl FromStr for Rule {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        //  If the current value is 0:
        //  <Behavior>
        //  If the current value is 1:
        //  <Behavior>
        let lines = s.lines().vec();
        let zero = lines[1..4].join("\n").parse()?;
        let one = lines[5..8].join("\n").parse()?;
        Ok(Self { zero, one })
    }
}

impl Rule {
    fn get(&self, value: bool) -> &Behavior {
        match value {
            false => &self.zero,
            true => &self.one,
        }
    }
}

#[derive(Debug)]
struct TuringMachine {
    state: u8,
    rules: HashMap<u8, Rule>,
    position: i16,
    tape: HashSet<i16>,
}

impl TuringMachine {
    fn step(&mut self) {
        let value = self.tape.contains(&self.position);
        let behavior = self.rules[&self.state].get(value);
        if behavior.write {
            self.tape.insert(self.position);
        } else {
            self.tape.remove(&self.position);
        }
        self.position += behavior.direction;
        self.state = behavior.next;
    }

    fn checksum(&self) -> usize {
        self.tape.len()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().full_groups();
    let (state, steps) = get_state(&groups[0]);
    let mut machine = TuringMachine {
        state,
        rules: groups.iter().skip(1).map(|group| get_rule(group)).collect(),
        position: 0,
        tape: HashSet::default(),
    };
    for _ in 0..steps {
        machine.step();
    }
    answer::part1(3099, machine.checksum());
}

fn get_state(s: &str) -> (u8, usize) {
    // Begin in state A.
    // Perform a diagnostic checksum after 12425180 steps.
    let [state, steps] = s.lines().array().unwrap();
    let [steps] = Parser::values(steps, " ").unwrap();
    (to_state(state), steps)
}

fn get_rule(s: &str) -> (u8, Rule) {
    // In state A:
    // <Rule>
    let (state, rule) = s.split_once('\n').unwrap();
    (to_state(state), rule.parse().unwrap())
}

fn to_state(s: &str) -> u8 {
    Convert::idx_upper(Convert::ch(last_word(s)))
}

fn last_word(s: &str) -> &str {
    Parser::nth_rev(s, " ", [0])[0]
}
