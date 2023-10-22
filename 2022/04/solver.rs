use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Section {
    start: i64,
    end: i64,
}

impl Section {
    fn from_str(section: &str) -> Self {
        let (start, end) = section.split_once("-").unwrap();
        Self {
            start: start.parse::<i64>().unwrap(),
            end: end.parse::<i64>().unwrap(),
        }
    }

    fn contains_all(&self, other: &Section) -> bool {
        self.start <= other.start && self.end >= other.end
    }

    fn contains_any(&self, other: &Section) -> bool {
        let max_start = self.start.max(other.start);
        let min_end = self.end.min(other.end);
        max_start <= min_end
    }
}

#[derive(Debug)]
struct Assignment {
    first: Section,
    second: Section,
}

impl Assignment {
    fn from_str(line: &str) -> Self {
        let (section_1, section_2) = line.split_once(",").unwrap();
        Assignment {
            first: Section::from_str(section_1),
            second: Section::from_str(section_2),
        }
    }

    fn full_overlap(&self) -> bool {
        self.first.contains_all(&self.second) || self.second.contains_all(&self.first)
    }

    fn any_overlap(&self) -> bool {
        self.first.contains_any(&self.second)
    }
}

fn main() {
    let assignments = reader::read(|line| Assignment::from_str(line));
    answer::part1(
        532,
        get_count(&assignments, |assignment| assignment.full_overlap()),
    );
    answer::part2(
        854,
        get_count(&assignments, |assignment| assignment.any_overlap()),
    );
}

fn get_count(assignments: &Vec<Assignment>, f: fn(&Assignment) -> bool) -> usize {
    assignments
        .iter()
        .filter(|assignment| f(assignment))
        .count()
}
