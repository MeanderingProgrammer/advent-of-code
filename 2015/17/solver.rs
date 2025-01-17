use aoc_lib::answer;
use aoc_lib::reader::Reader;
use itertools::Itertools;

fn main() {
    answer::timer(solution);
}

fn solution() {
    let capacities = Reader::default().read_int();
    let options = get_options(&capacities, 150);
    answer::part1(1304, options.len());
    answer::part2(18, num_min(&options));
}

fn get_options(capacities: &[i64], volume: i64) -> Vec<Vec<i64>> {
    (2..capacities.len())
        .flat_map(|i| capacities.iter().combinations(i))
        .map(|option| option.into_iter().cloned().collect())
        .filter(|option: &Vec<i64>| option.iter().sum::<i64>() == volume)
        .collect()
}

fn num_min(options: &[Vec<i64>]) -> usize {
    let lengths: Vec<usize> = options.iter().map(|option| option.len()).collect();
    let min = lengths.iter().min().unwrap();
    lengths.iter().filter(|length| *length == min).count()
}
