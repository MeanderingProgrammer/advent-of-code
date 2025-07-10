use aoc::prelude::*;
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

        match Str::enclosed(s, '"', '"') {
            Some(s) => Ok(Self::Letter(Str::first(s))),
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

impl FromStr for Rules {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut rules = HashMap::default();
        for line in s.lines() {
            let (number, rule) = line.split_once(": ").unwrap();
            rules.insert(number.parse().unwrap(), rule.parse().unwrap());
        }
        Ok(Self { rules })
    }
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
                .filter(|&input| Str::first(input) == *letter)
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
    let groups = Reader::default().groups::<String>();
    let mut rules = groups[0].parse().unwrap();
    answer::part1(198, total_matches(&rules, &groups[1]));
    rules.update(8, "42 | 42 8".parse().unwrap());
    rules.update(11, "42 31 | 42 11 31".parse().unwrap());
    answer::part2(372, total_matches(&rules, &groups[1]));
}

fn total_matches(rules: &Rules, s: &str) -> usize {
    s.lines().filter(|line| rules.matches(line)).count()
}
