use aoc::{HashMap, HashSet, Reader, Str, answer};

#[derive(Debug)]
struct Behavior {
    write: bool,
    direction: i16,
    next: u8,
}

impl From<&str> for Behavior {
    fn from(s: &str) -> Self {
        //    - Write the value 1.
        //    - Move one slot to the right.
        //    - Continue with state B.
        let lines = s.lines().collect::<Vec<_>>();
        let write = match last(lines[0], '.') {
            "0" => false,
            "1" => true,
            _ => unreachable!(),
        };
        let direction = match last(lines[1], '.') {
            "left" => -1,
            "right" => 1,
            _ => unreachable!(),
        };
        Self {
            write,
            direction,
            next: to_state(lines[2], '.'),
        }
    }
}

#[derive(Debug)]
struct Rule {
    zero: Behavior,
    one: Behavior,
}

impl From<&str> for Rule {
    fn from(s: &str) -> Self {
        //  If the current value is 0:
        //  <Behavior>
        //  If the current value is 1:
        //  <Behavior>
        let lines = s.lines().collect::<Vec<_>>();
        let zero = lines[1..4].join("\n").as_str().into();
        let one = lines[5..8].join("\n").as_str().into();
        Self { zero, one }
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
    let groups = Reader::default().groups::<String>();
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
    let lines = s.lines().collect::<Vec<_>>();
    (to_state(lines[0], '.'), Str::nth_rev(lines[1], ' ', 1))
}

fn get_rule(s: &str) -> (u8, Rule) {
    // In state A:
    // <Rule>
    let (state, rule) = s.split_once('\n').unwrap();
    (to_state(state, ':'), rule.into())
}

fn to_state(s: &str, trim: char) -> u8 {
    Str::lower_index(last(s, trim)) as u8
}

fn last(s: &str, trim: char) -> &str {
    s.split_whitespace().last().unwrap().trim_matches(trim)
}
