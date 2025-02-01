use aoc::{answer, Reader};

#[derive(Debug)]
struct Password {
    value: Vec<char>,
}

impl Password {
    fn only_increases(&self) -> bool {
        (0..(self.value.len() - 1)).all(|i| self.value[i + 1] >= self.value[i])
    }

    fn valid_p1(&self) -> bool {
        self.same_counts().into_iter().any(|count| count >= 2)
    }

    fn valid_p2(&self) -> bool {
        self.same_counts().contains(&2)
    }

    fn same_counts(&self) -> Vec<usize> {
        let mut result = Vec::default();
        let mut i = 0;
        while i < self.value.len() {
            let length = self.get_length_of_same(i);
            result.push(length);
            i += length;
        }
        result
    }

    fn get_length_of_same(&self, start: usize) -> usize {
        self.value
            .iter()
            .skip(start)
            .take_while(|ch| ch == &&self.value[start])
            .count()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let line = Reader::default().read_line();
    let values: Vec<usize> = line
        .split('-')
        .map(|value| value.parse().unwrap())
        .collect();
    let passwords: Vec<Password> = (values[0]..=values[1])
        .map(|value| Password {
            value: value.to_string().chars().collect(),
        })
        .filter(|pass| pass.only_increases())
        .collect();
    answer::part1(979, passwords.iter().filter(|pass| pass.valid_p1()).count());
    answer::part2(635, passwords.iter().filter(|pass| pass.valid_p2()).count());
}
