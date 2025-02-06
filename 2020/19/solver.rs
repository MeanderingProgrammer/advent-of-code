use aoc::{answer, Convert, HashMap, Parser, Reader};
use std::str::FromStr;

#[derive(Debug)]
enum Rule {
    Letter(char),
    And(Vec<i64>),
    Or(Vec<i64>, Vec<i64>),
}

impl FromStr for Rule {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        fn rule_list(s: &str) -> Vec<i64> {
            s.split(' ').map(|n| n.parse().unwrap()).collect()
        }

        match Parser::enclosed(s, '"', '"') {
            Some(s) => Ok(Self::Letter(Convert::ch(s))),
            None => {
                if s.contains('|') {
                    let (left, right) = s.split_once(" | ").unwrap();
                    Ok(Self::Or(rule_list(left), rule_list(right)))
                } else {
                    Ok(Self::And(rule_list(s)))
                }
            }
        }
    }
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
                .filter(|&input| Convert::ch(input) == *letter)
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
    let groups = Reader::default().groups();
    let mut rules = parse_rules(&groups[0]);
    answer::part1(198, total_matches(&rules, &groups[1]));
    rules.update(8, "42 | 42 8".parse().unwrap());
    rules.update(11, "42 31 | 42 11 31".parse().unwrap());
    answer::part2(372, total_matches(&rules, &groups[1]));
}

fn total_matches(rules: &Rules, lines: &[String]) -> usize {
    lines.iter().filter(|line| rules.matches(line)).count()
}

fn parse_rules(lines: &[String]) -> Rules {
    let mut result = HashMap::default();
    for line in lines.iter() {
        let [number, rule] = Parser::nth(line, ": ", [0, 1]);
        result.insert(number.parse().unwrap(), rule.parse().unwrap());
    }
    Rules { rules: result }
}
