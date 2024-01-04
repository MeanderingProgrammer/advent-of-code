use aoc_lib::answer;
use aoc_lib::reader;
use nom::{
    bytes::complete::tag,
    character::complete::{alpha0, digit0, newline},
    combinator::map_res,
    sequence::tuple,
    IResult,
};
use std::collections::HashMap;

#[derive(Debug)]
enum Direction {
    LEFT,
    RIGHT,
}

impl Direction {
    fn from_str(input: &str) -> Result<Self, String> {
        match input {
            "left" => Ok(Self::LEFT),
            "right" => Ok(Self::RIGHT),
            _ => Err(String::from("unhandled input")),
        }
    }

    fn value(&self) -> i64 {
        match self {
            Self::LEFT => -1,
            Self::RIGHT => 1,
        }
    }
}

#[derive(Debug)]
struct Behavior {
    write: u8,
    direction: Direction,
    next: String,
}

impl Behavior {
    fn from_str(input: &str) -> IResult<&str, Self> {
        //    - Write the value 1.
        //    - Move one slot to the right.
        //    - Continue with state B.
        let (input, write) = tuple((
            tag("    - Write the value "),
            map_res(digit0, |s: &str| s.parse::<u8>()),
            tag("."),
            newline,
        ))(input)?;
        let (input, direction) = tuple((
            tag("    - Move one slot to the "),
            map_res(alpha0, Direction::from_str),
            tag("."),
            newline,
        ))(input)?;
        let (input, next) = tuple((tag("    - Continue with state "), alpha0, tag(".")))(input)?;
        Ok((
            input,
            Self {
                write: write.1,
                direction: direction.1,
                next: next.1.to_string(),
            },
        ))
    }
}

#[derive(Debug)]
struct Rule {
    zero: Behavior,
    one: Behavior,
}

impl Rule {
    fn from_str(input: &str) -> IResult<&str, Self> {
        //  If the current value is 0:
        //  <Behavior>
        //  If the current value is 1:
        //  <Behavior>
        let (input, _) = tuple((tag("  If the current value is 0:"), newline))(input)?;
        let (input, zero) = Behavior::from_str(input)?;
        let (input, _) = newline(input)?;
        let (input, _) = tuple((tag("  If the current value is 1:"), newline))(input)?;
        let (input, one) = Behavior::from_str(input)?;
        Ok((input, Self { zero, one }))
    }

    fn get(&self, value: &u8) -> Option<&Behavior> {
        match value {
            0 => Some(&self.zero),
            1 => Some(&self.one),
            _ => None,
        }
    }
}

#[derive(Debug)]
struct TuringMachine {
    state: String,
    rules: HashMap<String, Rule>,
    position: i64,
    tape: HashMap<i64, u8>,
}

impl TuringMachine {
    fn new(state: String, rules: HashMap<String, Rule>) -> Self {
        Self {
            state,
            rules,
            position: 0,
            tape: HashMap::new(),
        }
    }

    fn step(&mut self) {
        let value = self.tape.get(&self.position).unwrap_or(&0);
        let behavior = self.rules.get(&self.state).unwrap().get(value).unwrap();
        self.tape.insert(self.position, behavior.write);
        self.position += behavior.direction.value();
        self.state = behavior.next.clone();
    }

    fn checksum(&self) -> i64 {
        let mut result: i64 = 0;
        for value in self.tape.values() {
            result += *value as i64
        }
        result
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = reader::read_full_groups();

    let (start_state, steps) = get_state(&groups[0]).unwrap().1;
    let mut rules = HashMap::new();
    groups.iter().skip(1).for_each(|group| {
        let (state, rule) = get_rule(group).unwrap().1;
        rules.insert(state.to_string(), rule);
    });

    let mut machine = TuringMachine::new(start_state.to_string(), rules);
    for _ in 0..steps {
        machine.step();
    }
    answer::part1(3099, machine.checksum());
}

fn get_state(input: &str) -> IResult<&str, (&str, usize)> {
    // Begin in state A.
    // Perform a diagnostic checksum after 12425180 steps.
    let (input, start_state) = tuple((tag("Begin in state "), alpha0, tag("."), newline))(input)?;
    let (input, steps) = tuple((
        tag("Perform a diagnostic checksum after "),
        map_res(digit0, |s: &str| s.parse::<usize>()),
        tag(" steps."),
    ))(input)?;
    Ok((input, (start_state.1, steps.1)))
}

fn get_rule(input: &str) -> IResult<&str, (&str, Rule)> {
    // In state A:
    // <Rule>
    let (input, state) = tuple((tag("In state "), alpha0, tag(":"), newline))(input)?;
    let (input, rule) = Rule::from_str(input)?;
    Ok((input, (state.1, rule)))
}
