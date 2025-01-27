use aoc_lib::answer;
use aoc_lib::ids::Base;
use aoc_lib::reader::Reader;
use fxhash::FxHashSet;

#[derive(Debug, Clone)]
enum Unit {
    Upper(u8),
    Lower(u8),
}

impl Unit {
    fn new(ch: char) -> Self {
        match ch.is_ascii_uppercase() {
            true => Self::Upper(Base::ch_upper(ch)),
            false => Self::Lower(Base::ch_lower(ch)),
        }
    }

    fn variant(&self) -> u8 {
        match self {
            Self::Upper(variant) => *variant,
            Self::Lower(variant) => *variant,
        }
    }

    fn collide(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Upper(v1), Self::Lower(v2)) => v1 == v2,
            (Self::Lower(v1), Self::Upper(v2)) => v1 == v2,
            (Self::Upper(_), Self::Upper(_)) => false,
            (Self::Lower(_), Self::Lower(_)) => false,
        }
    }
}

#[derive(Debug)]
struct Polymer {
    units: Vec<Unit>,
}

impl Polymer {
    fn react(&mut self) -> usize {
        while let Some(i) = self.next() {
            self.units.remove(i);
            self.units.remove(i);
        }
        self.units.len()
    }

    #[allow(clippy::manual_find)]
    fn next(&self) -> Option<usize> {
        for i in 0..self.units.len() - 1 {
            if self.units[i].collide(&self.units[i + 1]) {
                return Some(i);
            }
        }
        None
    }

    fn variants(&self) -> FxHashSet<u8> {
        self.units.iter().map(|unit| unit.variant()).collect()
    }

    fn remove(&self, variant: u8) -> Self {
        let mut units = self.units.clone();
        units.retain(|unit| unit.variant() != variant);
        Self { units }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let chars = Reader::default().read_chars();
    let units: Vec<Unit> = chars.into_iter().map(Unit::new).collect();
    let mut polymer = Polymer { units };
    answer::part1(11242, polymer.react());
    answer::part2(5492, best_removed(&polymer));
}

fn best_removed(polymer: &Polymer) -> usize {
    polymer
        .variants()
        .into_iter()
        .map(|variant| polymer.remove(variant).react())
        .min()
        .unwrap()
}
