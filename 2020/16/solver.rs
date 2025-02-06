use aoc::{answer, Parser, Reader};
use std::str::FromStr;

#[derive(Debug)]
struct Range(usize, usize);

impl FromStr for Range {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // 1-3
        let [start, end] = Parser::values(s, "-").unwrap();
        Ok(Self(start, end))
    }
}

impl Range {
    fn contains(&self, value: usize) -> bool {
        value >= self.0 && value <= self.1
    }
}

#[derive(Debug)]
struct Rule {
    name: String,
    ranges: [Range; 2],
}

impl FromStr for Rule {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // class: <Value> or <Value>
        let [name, s] = Parser::all(s, ": ").unwrap();
        Ok(Self {
            name: name.to_string(),
            ranges: Parser::values(s, " or ").unwrap(),
        })
    }
}

impl Rule {
    fn matches(&self, value: usize) -> bool {
        self.ranges.iter().any(|range| range.contains(value))
    }
}

#[derive(Debug)]
struct Ticket {
    values: Vec<usize>,
}

impl FromStr for Ticket {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let values = s.split(',').map(|value| value.parse().unwrap()).collect();
        Ok(Self { values })
    }
}

impl Ticket {
    fn unmatched(&self, rules: &[Rule]) -> Vec<usize> {
        self.values
            .iter()
            .copied()
            .filter(|value| !rules.iter().any(|rule| rule.matches(*value)))
            .collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups: Vec<Vec<String>> = Reader::default().groups();
    let rules: Vec<Rule> = groups[0].iter().map(|line| line.parse().unwrap()).collect();
    let mine: Ticket = groups[1][1].parse().unwrap();
    let nearby: Vec<Ticket> = groups[2]
        .iter()
        .skip(1)
        .map(|line| line.parse().unwrap())
        .collect();
    answer::part1(26980, part1(&rules, &nearby));
    answer::part2(3021381607403, part2(&rules, &mine, &nearby));
}

fn part1(rules: &[Rule], nearby: &[Ticket]) -> usize {
    let mut unmatched: Vec<usize> = Vec::default();
    for ticket in nearby {
        unmatched.append(&mut ticket.unmatched(rules));
    }
    unmatched.into_iter().sum()
}

fn part2(rules: &[Rule], mine: &Ticket, nearby: &[Ticket]) -> usize {
    let tickets: Vec<&Ticket> = nearby
        .iter()
        .filter(|ticket| ticket.unmatched(rules).is_empty())
        .collect();

    let n = rules.len();
    assert_eq!(n, mine.values.len());
    for ticket in tickets.iter() {
        assert_eq!(n, ticket.values.len());
    }

    // rows[i] = row associated with rules[i]
    let mut rows: Vec<Option<usize>> = vec![None; n];
    while rows.iter().any(|row| row.is_none()) {
        for i in 0..n {
            let values: Vec<usize> = tickets.iter().map(|ticket| ticket.values[i]).collect();

            let mut candidates: Vec<usize> = rows
                .iter()
                .enumerate()
                .filter(|(_, row)| row.is_none())
                .map(|(i, _)| i)
                .collect();
            for value in values {
                candidates.retain(|i| rules[*i].matches(value));
            }
            if candidates.len() == 1 {
                rows[candidates.pop().unwrap()] = Some(i);
            }
        }
    }

    let rows: Vec<usize> = rows.into_iter().map(|row| row.unwrap()).collect();
    rules
        .iter()
        .enumerate()
        .filter(|(_, rule)| rule.name.starts_with("departure"))
        .map(|(i, _)| rows[i])
        .map(|i| mine.values[i])
        .product()
}
