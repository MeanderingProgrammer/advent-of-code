use aoc_lib::answer;
use aoc_lib::reader;

#[derive(Debug)]
struct Section {
    start: i64,
    end: i64,
}

impl Section {
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
    fn full_overlap(&self) -> bool {
        self.first.contains_all(&self.second) || self.second.contains_all(&self.first)
    }

    fn any_overlap(&self) -> bool {
        self.first.contains_any(&self.second)
    }
}

fn main() {
    let assignments = reader::read(|line| {
        let (section_1, section_2) = line.split_once(",").unwrap();
        Assignment {
            first: to_section(section_1.to_string()),
            second: to_section(section_2.to_string()),
        }
    });
    answer::part1(
        532,
        assignments
            .iter()
            .filter(|assignment| assignment.full_overlap())
            .count(),
    );
    answer::part2(
        854,
        assignments
            .iter()
            .filter(|assignment| assignment.any_overlap())
            .count(),
    );
}

fn to_section(section: String) -> Section {
    let (start, end) = section.split_once("-").unwrap();
    Section {
        start: start.parse::<i64>().unwrap(),
        end: end.parse::<i64>().unwrap(),
    }
}
