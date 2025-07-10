use aoc::prelude::*;

#[derive(Debug, PartialEq, Eq, Hash)]
struct Square(Vec<String>);

impl Square {
    // Evolution: 3x3 -> 4x4 -> 6x6 -> 9x9 => 9 3x3
    // Once we hit 9x9 we can divide into 9 independent 3x3 sections
    // that are independent and repeat the same pattern
    fn next(&self, patterns: &Patterns) -> Vec<Self> {
        let rows: Vec<String> = self
            .components()
            .into_iter()
            .map(|row| row.iter().map(|square| patterns.get(square)).collect())
            .flat_map(Self::join)
            .collect();
        if rows.len() == 9 {
            Self(rows)
                .components()
                .into_iter()
                .flat_map(|row| row.into_iter().map(Square))
                .collect()
        } else {
            vec![Self(rows)]
        }
    }

    fn components(&self) -> Vec<Vec<Vec<String>>> {
        let n = self.0.len();
        let size = if n % 2 == 0 { 2 } else { 3 };
        let iter = (0..n).step_by(size);
        iter.clone()
            .map(|r| iter.clone().map(|c| self.lines(r, c, size)).collect())
            .collect()
    }

    fn lines(&self, r: usize, c: usize, size: usize) -> Vec<String> {
        self.0[r..r + size]
            .iter()
            .map(|line| line[c..c + size].to_string())
            .collect()
    }

    fn join(row: Vec<Vec<String>>) -> Vec<String> {
        (0..row[0].len())
            .map(|i| row.iter().map(|square| square[i].clone()).collect())
            .map(|l: Vec<String>| l.join(""))
            .collect()
    }

    fn on(&self) -> usize {
        self.0
            .iter()
            .flat_map(|row| row.chars())
            .filter(|ch| *ch == '#')
            .count()
    }
}

#[derive(Debug)]
struct Art {
    sections: HashMap<Square, usize>,
}

impl Art {
    fn new(values: &[&str]) -> Self {
        let square = Square(values.iter().map(|row| row.to_string()).collect());
        let mut sections = HashMap::default();
        sections.insert(square, 1);
        Self { sections }
    }

    fn next(&self, patterns: &Patterns) -> Self {
        let mut sections = HashMap::default();
        for (square, count) in self.sections.iter() {
            for next in square.next(patterns) {
                *sections.entry(next).or_default() += count;
            }
        }
        Self { sections }
    }

    fn on(&self) -> usize {
        self.sections
            .iter()
            .map(|(square, count)| square.on() * count)
            .sum()
    }
}

#[derive(Debug, Default)]
struct Patterns(HashMap<Vec<String>, Vec<String>>);

impl Patterns {
    fn add(&mut self, key: &Grid<char>, value: Vec<String>) {
        let lines = key
            .to_string()
            .split('\n')
            .map(|line| line.to_string())
            .collect();
        self.0.insert(lines, value);
    }

    fn get(&self, key: &Vec<String>) -> Vec<String> {
        self.0.get(key).unwrap().clone()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().lines();
    let patterns = get_patterns(&lines);
    answer::part1(188, run(&patterns, 5));
    answer::part2(2758764, run(&patterns, 18));
}

fn get_patterns(lines: &[String]) -> Patterns {
    let mut patterns = Patterns::default();
    for line in lines {
        let (input, output) = line.split_once(" => ").unwrap();
        let input: Vec<String> = input.split("/").map(|row| row.to_string()).collect();
        let output: Vec<String> = output.split("/").map(|row| row.to_string()).collect();
        let mut grid = (&input).into();
        for _ in 0..4 {
            patterns.add(&grid, output.clone());
            patterns.add(&grid.transform(|p| Point::new(-p.x, p.y)), output.clone());
            grid = grid.transform(|p| Point::new(-p.y, p.x));
        }
    }
    patterns
}

fn run(patterns: &Patterns, n: usize) -> usize {
    let mut art = Art::new(&[".#.", "..#", "###"]);
    for _ in 0..n {
        art = art.next(patterns);
    }
    art.on()
}
