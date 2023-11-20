use aoc_lib::answer;
use aoc_lib::reader;
use std::collections::HashSet;

#[derive(Debug)]
struct Polymer {
    units: Vec<char>,
}

impl Polymer {
    fn react(&mut self) -> usize {
        while let Some(reaction_index) = self.get_reaction_index() {
            self.units.remove(reaction_index);
            self.units.remove(reaction_index);
        }
        self.units.len()
    }

    fn get_reaction_index(&self) -> Option<usize> {
        for i in 0..self.units.len() - 1 {
            let (u1, u2) = (self.units[i], self.units[i + 1]);
            if Self::collide(u1, u2) {
                return Some(i);
            }
        }
        None
    }

    fn get_unit_types(&self) -> HashSet<char> {
        self.units
            .iter()
            .map(|unit| unit.to_ascii_lowercase())
            .collect()
    }

    fn remove_unit_type(&self, unit_type: char) -> Self {
        let mut unit_copy = self.units.clone();
        unit_copy.retain(|&unit| unit.to_ascii_lowercase() != unit_type);
        Self { units: unit_copy }
    }

    fn collide(u1: char, u2: char) -> bool {
        u1.is_lowercase() != u2.is_lowercase() && u1.to_ascii_lowercase() == u2.to_ascii_lowercase()
    }
}

fn main() {
    let mut polymer = Polymer {
        units: reader::read_chars(),
    };
    answer::part1(11242, polymer.react());
    answer::part2(5492, best_removed(&polymer));
}

fn best_removed(polymer: &Polymer) -> usize {
    polymer
        .get_unit_types()
        .into_iter()
        .map(|unit_type| polymer.remove_unit_type(unit_type).react())
        .min()
        .unwrap()
}
