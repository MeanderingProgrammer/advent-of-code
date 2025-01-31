use aoc_lib::answer;
use aoc_lib::collections::HashMap;
use aoc_lib::reader::Reader;

#[derive(Debug)]
enum Operation {
    Add,
    Subtract,
    Multiply,
    Divide,
}

impl Operation {
    fn new(value: &str) -> Self {
        match value {
            "+" => Operation::Add,
            "-" => Operation::Subtract,
            "*" => Operation::Multiply,
            "/" => Operation::Divide,
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
enum Expression {
    SpecificNumber(i64),
    MathOperation(String, Operation, String),
}

impl Expression {
    fn new(parts: Vec<&str>) -> Self {
        match parts.len() {
            1 => Self::SpecificNumber(parts[0].parse::<i64>().unwrap()),
            3 => Self::MathOperation(
                parts[0].to_string(),
                Operation::new(parts[1]),
                parts[2].to_string(),
            ),
            _ => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct Monkeys {
    monkeys: HashMap<String, Expression>,
}

impl Monkeys {
    fn new(lines: Vec<String>) -> Self {
        let mut monkeys = HashMap::default();
        lines.iter().for_each(|line| {
            let (name, job) = line.split_once(": ").unwrap();
            monkeys.insert(name.to_string(), Expression::new(job.split(' ').collect()));
        });
        Monkeys { monkeys }
    }

    fn get(&self, name: &str) -> &Expression {
        self.monkeys.get(name).unwrap()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let monkeys = Monkeys::new(Reader::default().read_lines());
    answer::part1(81075092088442, evaluate(&monkeys, "root"));
    answer::part2(3349136384441, evaluate_human(&monkeys));
}

fn evaluate(monkeys: &Monkeys, name: &str) -> i64 {
    match monkeys.get(name) {
        Expression::SpecificNumber(value) => *value,
        Expression::MathOperation(left_name, operation, right_name) => {
            let left_value = evaluate(monkeys, left_name);
            let right_value = evaluate(monkeys, right_name);
            match operation {
                Operation::Add => left_value + right_value,
                Operation::Subtract => left_value - right_value,
                Operation::Multiply => left_value * right_value,
                Operation::Divide => left_value / right_value,
            }
        }
    }
}

fn evaluate_human(monkeys: &Monkeys) -> i64 {
    let (to_process, to_calculate) = match monkeys.get("root") {
        Expression::MathOperation(left_name, _, right_name) => {
            if depends_on_human(monkeys, left_name) {
                (left_name, right_name)
            } else {
                (right_name, left_name)
            }
        }
        _ => unreachable!(),
    };
    process_human(monkeys, to_process, evaluate(monkeys, to_calculate))
}

fn process_human(monkeys: &Monkeys, name: &str, value: i64) -> i64 {
    if name == "humn" {
        return value;
    }
    match monkeys.get(name) {
        Expression::MathOperation(left_name, operation, right_name) => {
            let (new_name, new_value) = if depends_on_human(monkeys, left_name) {
                let right_value = evaluate(monkeys, right_name);
                (
                    left_name,
                    match operation {
                        // left + right = value -> left = value - right
                        Operation::Add => value - right_value,
                        // left - right = value -> left = value + right
                        Operation::Subtract => value + right_value,
                        // left * right = value -> left = value / right
                        Operation::Multiply => value / right_value,
                        // left / right = value -> left = value * right
                        Operation::Divide => value * right_value,
                    },
                )
            } else {
                let left_value = evaluate(monkeys, left_name);
                (
                    right_name,
                    match operation {
                        // left + right = value -> right = value - left
                        Operation::Add => value - left_value,
                        // left - right = value -> right = left - value
                        Operation::Subtract => left_value - value,
                        // left * right = value -> right = value / left
                        Operation::Multiply => value / left_value,
                        // left / right = value -> right = value * right
                        Operation::Divide => left_value * value,
                    },
                )
            };
            process_human(monkeys, new_name, new_value)
        }
        _ => unreachable!(),
    }
}

fn depends_on_human(monkeys: &Monkeys, name: &str) -> bool {
    if name == "humn" {
        return true;
    }
    match monkeys.get(name) {
        Expression::SpecificNumber(_) => false,
        Expression::MathOperation(left_name, _, right_name) => {
            depends_on_human(monkeys, left_name) || depends_on_human(monkeys, right_name)
        }
    }
}
