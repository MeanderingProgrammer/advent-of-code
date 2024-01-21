use aoc_lib::answer;
use aoc_lib::reader::Reader;
use regex::Regex;
use std::cmp::Reverse;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, PartialEq)]
enum Category {
    Immune,
    Infection,
}

impl Category {
    fn enemy(&self) -> Self {
        match self {
            Self::Immune => Self::Infection,
            Self::Infection => Self::Immune,
        }
    }
}

#[derive(Debug, Clone)]
struct Group {
    id: usize,
    category: Category,
    units: i64,
    hp: i64,
    weaknesses: HashSet<String>,
    immunities: HashSet<String>,
    damage: i64,
    damage_type: String,
    initiative: i64,
}

impl Group {
    fn dead(&self) -> bool {
        self.units <= 0
    }

    fn power(&self) -> i64 {
        self.units * self.damage
    }

    fn calculate_damage(&self, o: &Group) -> i64 {
        if o.immunities.contains(&self.damage_type) {
            0
        } else if o.weaknesses.contains(&self.damage_type) {
            self.power() * 2
        } else {
            self.power()
        }
    }

    fn to_choose(&self) -> (i64, i64) {
        (self.power(), self.initiative)
    }

    fn to_target(&self, o: &Group) -> (i64, i64, i64) {
        (self.calculate_damage(o), o.power(), o.initiative)
    }

    fn hit(&mut self, damage: i64) {
        self.units -= damage / self.hp;
    }
}

#[derive(Debug)]
struct Battle {
    groups: Vec<Group>,
}

impl Battle {
    fn simulate(&mut self) {
        let mut previous = -1;
        let mut current = 0;
        while !self.groups.is_empty() && previous != current {
            self.attack();
            previous = current;
            current = self.winning_units();
        }
    }

    fn attack(&mut self) {
        self.groups.sort_by_key(|group| Reverse(group.to_choose()));
        let mut assignments = self.assign_targets().clone();
        assignments.sort_by_key(|(id, _)| Reverse(self.get_by_id(*id).initiative));
        for (group_id, target_id) in assignments.into_iter() {
            let group = self.get_by_id(group_id).clone();
            if !group.dead() {
                let target_index = self.groups.iter().position(|g| g.id == target_id).unwrap();
                let target = self.groups.get_mut(target_index).unwrap();
                let damage = group.calculate_damage(&target);
                target.hit(damage);
            }
        }
        self.groups = self
            .groups
            .iter()
            .filter(|group| !group.dead())
            .map(|group| group.clone())
            .collect();
    }

    fn assign_targets(&self) -> Vec<(usize, usize)> {
        let mut assignments = Vec::new();
        let mut targets = HashSet::new();
        for group in self.groups.iter() {
            match self.get_target(group, &targets) {
                None => (),
                Some(target) => {
                    assignments.push((group.id, target.id));
                    targets.insert(target.id);
                }
            }
        }
        assignments
    }

    fn get_target(&self, group: &Group, targets: &HashSet<usize>) -> Option<&Group> {
        self.get_category(group.category.enemy())
            .into_iter()
            .filter(|target| !targets.contains(&target.id))
            .filter(|target| group.calculate_damage(target) > 0)
            .max_by_key(|target| group.to_target(target))
    }

    fn get_category(&self, c: Category) -> Vec<&Group> {
        self.groups.iter().filter(|g| g.category == c).collect()
    }

    fn get_by_id(&self, id: usize) -> &Group {
        self.groups.iter().find(|g| g.id == id).unwrap()
    }

    fn immune_won(&self) -> bool {
        let immune = self.get_category(Category::Immune);
        let infection = self.get_category(Category::Infection);
        !immune.is_empty() && infection.is_empty()
    }

    fn winning_units(&self) -> i64 {
        self.groups.iter().map(|group| group.units).sum()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    answer::part1(16086, part_1());
    answer::part2(3957, part_2().unwrap());
}

fn part_1() -> i64 {
    let mut battle = get_battle(0);
    battle.simulate();
    battle.winning_units()
}

fn part_2() -> Option<i64> {
    (1..).into_iter().find_map(|boost| {
        let mut battle = get_battle(boost);
        battle.simulate();
        if battle.immune_won() {
            Some(battle.winning_units())
        } else {
            None
        }
    })
}

fn get_battle(boost: i64) -> Battle {
    fn parse_group(id: usize, category: Category, raw: &str, boost: i64) -> Group {
        let re = Regex::new(r"\((.*)\)").unwrap();
        let mut traits: HashMap<String, HashSet<String>> = HashMap::new();
        if let Some(captures) = re.captures(raw) {
            for raw_trait in captures.get(1).unwrap().as_str().split("; ") {
                let (trait_type, trait_values) = raw_trait.split_once(" to ").unwrap();
                traits.insert(
                    trait_type.to_string(),
                    trait_values.split(", ").map(|s| s.to_string()).collect(),
                );
            }
        }
        let parts: Vec<&str> = raw.split_whitespace().collect();
        Group {
            id,
            category,
            units: parts[0].parse().unwrap(),
            hp: parts[4].parse().unwrap(),
            weaknesses: traits.get("weak").unwrap_or(&HashSet::new()).clone(),
            immunities: traits.get("immune").unwrap_or(&HashSet::new()).clone(),
            damage: parts[parts.len() - 6].parse::<i64>().unwrap() + boost,
            damage_type: parts[parts.len() - 5].to_string(),
            initiative: parts[parts.len() - 1].parse().unwrap(),
        }
    }

    let mut groups = Vec::new();
    let line_groups = Reader::default().read_group_lines();
    for value in line_groups[0].iter().skip(1) {
        groups.push(parse_group(groups.len(), Category::Immune, value, boost));
    }
    for value in line_groups[1].iter().skip(1) {
        groups.push(parse_group(groups.len(), Category::Infection, value, 0));
    }
    Battle { groups }
}
