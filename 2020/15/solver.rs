use aoc::{answer, HashMap, Reader};

fn main() {
    answer::timer(solution);
}

fn solution() {
    let values: Vec<usize> = Reader::default()
        .read_csv()
        .into_iter()
        .map(|value| value as usize)
        .collect();
    answer::part1(240, run(&values, 2_020, 1_000));
    answer::part2(505, run(&values, 30_000_000, 5_000_000));
}

fn run(values: &[usize], n: usize, split: usize) -> usize {
    let mut small: Vec<u32> = vec![0; split];
    let mut large: HashMap<usize, u32> = HashMap::default();
    for i in 0..values.len() - 1 {
        small[values[i]] = (i + 1) as u32;
    }
    let mut current: usize = *values.last().unwrap();
    for i in values.len()..n {
        let previous = if current < split {
            let value = small[current];
            small[current] = i as u32;
            value as usize
        } else {
            large.insert(current, i as u32).unwrap_or(0) as usize
        };
        current = if previous == 0 { 0 } else { i - previous };
    }
    current
}
