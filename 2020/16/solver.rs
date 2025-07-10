use aoc::prelude::*;

#[derive(Debug)]
struct Range(usize, usize);

impl From<&str> for Range {
    fn from(s: &str) -> Self {
        // 1-3
        let (start, end) = s.split_once('-').unwrap();
        Self(start.parse().unwrap(), end.parse().unwrap())
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

impl From<&str> for Rule {
    fn from(s: &str) -> Self {
        // class: <Value> or <Value>
        let (name, s) = s.split_once(": ").unwrap();
        let (r1, r2) = s.split_once(" or ").unwrap();
        Self {
            name: name.to_string(),
            ranges: [r1.into(), r2.into()],
        }
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

impl From<&str> for Ticket {
    fn from(s: &str) -> Self {
        let values = s.split(',').map(|value| value.parse().unwrap()).collect();
        Self { values }
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
    let groups = Reader::default().groups::<String>();
    let rules: Vec<Rule> = groups[0].lines().map(|line| line.into()).collect();
    let mine: Ticket = groups[1].lines().last().unwrap().into();
    let nearby: Vec<Ticket> = groups[2].lines().skip(1).map(|line| line.into()).collect();
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
