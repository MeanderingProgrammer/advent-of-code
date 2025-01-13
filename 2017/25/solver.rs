use aoc_lib::answer;
use aoc_lib::ids::Base;
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;
use std::str::FromStr;

#[derive(Debug)]
enum Direction {
    Left,
    Right,
}

impl FromStr for Direction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "left" => Ok(Self::Left),
            "right" => Ok(Self::Right),
            _ => Err(String::from("unhandled input")),
        }
    }
}

impl Direction {
    fn value(&self) -> i64 {
        match self {
            Self::Left => -1,
            Self::Right => 1,
        }
    }
}

#[derive(Debug)]
struct Behavior {
    write: u8,
    direction: Direction,
    next: u8,
}

impl FromStr for Behavior {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        //    - Write the value 1.
        //    - Move one slot to the right.
        //    - Continue with state B.
        let lines: Vec<&str> = s.lines().collect();
        Ok(Self {
            write: last_word(lines[0]).parse().unwrap(),
            direction: last_word(lines[1]).parse()?,
            next: to_state(lines[2]),
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
        let lines: Vec<&str> = s.lines().collect();
        let zero = Behavior::from_str(&lines[1..4].join("\n"))?;
        let one = Behavior::from_str(&lines[5..8].join("\n"))?;
        Ok(Self { zero, one })
    }
}

impl Rule {
    fn get(&self, value: &u8) -> &Behavior {
        match value {
            0 => &self.zero,
            1 => &self.one,
            _ => panic!("Unhandled value: {value}"),
        }
    }
}

#[derive(Debug)]
struct TuringMachine {
    state: u8,
    rules: FxHashMap<u8, Rule>,
    position: i64,
    tape: FxHashMap<i64, u8>,
}

impl TuringMachine {
    fn step(&mut self) {
        let value = self.tape.get(&self.position).unwrap_or(&0);
        let behavior = self.rules[&self.state].get(value);
        self.tape.insert(self.position, behavior.write);
        self.position += behavior.direction.value();
        self.state = behavior.next;
    }

    fn checksum(&self) -> usize {
        self.tape.values().filter(|value| **value == 1).count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().read_full_groups();
    let (state, steps) = get_state(&groups[0]);
    let mut machine = TuringMachine {
        state,
        rules: groups.iter().skip(1).map(|group| get_rule(group)).collect(),
        position: 0,
        tape: FxHashMap::default(),
    };
    for _ in 0..steps {
        machine.step();
    }
    answer::part1(3099, machine.checksum());
}

fn get_state(s: &str) -> (u8, usize) {
    // Begin in state A.
    // Perform a diagnostic checksum after 12425180 steps.
    let lines: Vec<&str> = s.lines().collect();
    let steps = lines[1].split_whitespace().nth(5).unwrap();
    (to_state(lines[0]), steps.parse().unwrap())
}

fn get_rule(s: &str) -> (u8, Rule) {
    // In state A:
    // <Rule>
    let (state, rule) = s.split_once('\n').unwrap();
    (to_state(state), rule.parse().unwrap())
}

fn to_state(s: &str) -> u8 {
    Base::ch_upper(last_word(s).chars().next().unwrap())
}

fn last_word(s: &str) -> &str {
    let word = s.split_whitespace().last().unwrap();
    &word[..word.len() - 1]
}
