use aoc::{answer, Iter, Reader};

#[derive(Debug)]
struct Masking {
    values: Vec<i64>,
    preamble: usize,
}

impl Masking {
    fn first_invalid(&self) -> i64 {
        self.values
            .iter()
            .enumerate()
            .skip(self.preamble)
            .find(|(i, _)| !self.can_sum(*i))
            .map(|(_, value)| *value)
            .unwrap()
    }

    fn can_sum(&self, i: usize) -> bool {
        let target = self.values[i];
        let preamble: Vec<i64> = self
            .values
            .iter()
            .skip(i - self.preamble)
            .take(self.preamble)
            .copied()
            .collect();
        preamble
            .iter()
            .map(|value| target - *value)
            .any(|need| preamble.contains(&need))
    }

    fn sum_set(&self, target: i64) -> Vec<i64> {
        for i in 0..self.values.len() {
            for j in i + 1..self.values.len() {
                let subset = &self.values[i..j];
                let total: i64 = subset.iter().sum();
                if total == target {
                    return subset.to_vec();
                }
                if total > target {
                    break;
                }
            }
        }
        unreachable!()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let masking = Masking {
        values: Reader::default().lines(),
        preamble: 25,
    };
    let invalid = masking.first_invalid();
    let sum_set = masking.sum_set(invalid);
    let (min, max) = sum_set.into_iter().minmax().unwrap();
    answer::part1(104054607, invalid);
    answer::part2(13935797, min + max);
}
