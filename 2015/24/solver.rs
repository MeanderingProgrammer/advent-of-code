use aoc_lib::answer;
use aoc_lib::reader::Reader;
use itertools::Itertools;

#[derive(Debug)]
struct Organizer {
    weights: Vec<usize>,
}

impl Organizer {
    fn run(&self, sections: usize) -> usize {
        let total: usize = self.weights.iter().sum();
        let target = total / sections;
        (1..=self.weights.len())
            .map(|k| self.combinations(k, target))
            .find(|combinations| !combinations.is_empty())
            .unwrap()
            .into_iter()
            .map(|weights| weights.into_iter().product::<usize>())
            .min()
            .unwrap()
    }

    fn combinations(&self, k: usize, target: usize) -> Vec<Vec<usize>> {
        self.weights
            .iter()
            .combinations(k)
            .map(|weights| weights.into_iter().copied().collect())
            .filter(|weights: &Vec<usize>| weights.iter().sum::<usize>() == target)
            .collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let weights = Reader::default().read_from_str();
    let organizer = Organizer { weights };
    answer::part1(10439961859, organizer.run(3));
    answer::part2(72050269, organizer.run(4));
}
