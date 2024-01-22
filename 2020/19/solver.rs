use aoc_lib::answer;
use aoc_lib::reader::Reader;
use std::collections::HashMap;

#[derive(Debug)]
enum Rule {
    Letter(char),
    And(Vec<i64>),
    Or(Vec<i64>, Vec<i64>),
}

#[derive(Debug)]
struct Rules {
    rules: HashMap<i64, Rule>,
}

impl Rules {
    fn matches(&self, input: &str) -> bool {
        self.remainders(vec![input], 0)
            .iter()
            .any(|remainder| remainder.is_empty())
    }

    fn remainders<'a>(&'a self, inputs: Vec<&'a str>, rule_number: i64) -> Vec<&'a str> {
        if inputs.is_empty() {
            return inputs;
        }
        match self.rules.get(&rule_number).unwrap() {
            Rule::Letter(letter) => inputs
                .into_iter()
                .filter(|&input| !input.is_empty())
                .filter(|&input| input.chars().nth(0).unwrap() == *letter)
                .map(|input| &input[1..])
                .collect(),
            Rule::And(rules) => self.matching(inputs, rules),
            Rule::Or(left, right) => {
                let mut result = vec![];
                result.append(&mut self.matching(inputs.clone(), left));
                result.append(&mut self.matching(inputs.clone(), right));
                result
            }
        }
    }

    fn matching<'a>(&'a self, inputs: Vec<&'a str>, rules: &[i64]) -> Vec<&'a str> {
        let mut result = inputs;
        for rule in rules.iter() {
            result = self.remainders(result, *rule);
        }
        result
    }

    fn update(&mut self, rule_number: i64, rule: Rule) {
        self.rules.insert(rule_number, rule);
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().read_group_lines();
    let mut rules = parse_rules(&groups[0]);
    answer::part1(198, total_matches(&rules, &groups[1]));
    rules.update(8, parse_rule("42 | 42 8"));
    rules.update(11, parse_rule("42 31 | 42 11 31"));
    answer::part2(372, total_matches(&rules, &groups[1]));
}

fn total_matches(rules: &Rules, lines: &[String]) -> usize {
    lines.iter().filter(|line| rules.matches(line)).count()
}

fn parse_rules(lines: &[String]) -> Rules {
    let mut result = HashMap::new();
    for line in lines.iter() {
        let (number, rule) = line.split_once(": ").unwrap();
        result.insert(number.parse().unwrap(), parse_rule(rule));
    }
    Rules { rules: result }
}

fn parse_rule(line: &str) -> Rule {
    if line.len() == 3 && line.starts_with('\"') && line.ends_with('\"') {
        Rule::Letter(line.as_bytes()[1] as char)
    } else if line.contains('|') {
        let (left, right) = line.split_once(" | ").unwrap();
        Rule::Or(rule_list(left), rule_list(right))
    } else {
        Rule::And(rule_list(line))
    }
}

fn rule_list(s: &str) -> Vec<i64> {
    s.split(' ').map(|n| n.parse().unwrap()).collect()
}
