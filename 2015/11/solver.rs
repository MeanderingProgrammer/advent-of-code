use aoc::{Char, HashSet, Reader, answer};

#[derive(Debug)]
struct PasswordGenerator {
    value: Vec<u8>,
}

impl PasswordGenerator {
    fn new(value: String) -> Self {
        Self {
            value: value.chars().map(Char::lower_index).collect(),
        }
    }

    fn next(&mut self) {
        let index = match self.last_index_under(25) {
            None => {
                self.value.insert(0, 0);
                0
            }
            Some(index) => {
                self.value[index] += 1;
                index
            }
        };
        ((index + 1)..self.value.len()).for_each(|i| self.value[i] = 0);
    }

    fn last_index_under(&self, n: u8) -> Option<usize> {
        (0..self.value.len()).rev().find(|&i| self.value[i] < n)
    }

    fn valid(&self) -> bool {
        self.contains_triple() && !self.contains_invalid() && self.num_pairs() > 1
    }

    fn contains_triple(&self) -> bool {
        (0..self.value.len() - 2).any(|i| {
            self.value[i] + 1 == self.value[i + 1] && self.value[i] + 2 == self.value[i + 2]
        })
    }

    fn contains_invalid(&self) -> bool {
        let invalid = HashSet::from_iter(['i', 'o', 'l'].map(Char::lower_index));
        let value = HashSet::from_iter(self.value.iter().cloned());
        invalid.intersection(&value).count() > 0
    }

    fn num_pairs(&self) -> usize {
        let pairs: HashSet<u8> = (0..self.value.len() - 1)
            .filter(|&i| self.value[i] == self.value[i + 1])
            .map(|i| self.value[i])
            .collect();
        pairs.len()
    }

    fn get_value(&self) -> String {
        self.value.iter().map(|i| Char::lower_char(*i)).collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let value = Reader::default().line();
    let mut generator = PasswordGenerator::new(value);
    answer::part1("hxbxxyzz", &run(&mut generator));
    answer::part2("hxcaabcc", &run(&mut generator));
}

fn run(generator: &mut PasswordGenerator) -> String {
    generator.next();
    while !generator.valid() {
        generator.next();
    }
    generator.get_value()
}
