use aoc::{answer, HashMap, HashSet, Parser, Reader};
use std::cmp::Reverse;

#[derive(Debug, Clone, PartialEq)]
enum Kind {
    Immune,
    Infection,
}

impl Kind {
    fn enemy(&self) -> Self {
        match self {
            Self::Immune => Self::Infection,
            Self::Infection => Self::Immune,
        }
    }
}

#[derive(Debug, Clone)]
struct Army {
    id: usize,
    kind: Kind,
    units: i64,
    hp: i64,
    weaknesses: HashSet<String>,
    immunities: HashSet<String>,
    damage: i64,
    damage_type: String,
    initiative: i64,
}

impl Army {
    fn new(id: usize, kind: Kind, s: &str) -> Self {
        // 18 units each with 729 hit points <traits> with an attack that does 8 radiation damage at initiative 10
        let [units, hp, damage, initiative] = Parser::values(s, " ").unwrap();
        let [damage_type] = Parser::nth_rev(s, " ", [4]);
        let mut traits = Self::traits(s);
        let weaknesses = traits.remove("weak").unwrap_or_default();
        let immunities = traits.remove("immune").unwrap_or_default();
        Self {
            id,
            kind,
            units,
            hp,
            weaknesses,
            immunities,
            damage,
            damage_type: damage_type.to_string(),
            initiative,
        }
    }

    fn traits(s: &str) -> HashMap<String, HashSet<String>> {
        // (weak to fire; immune to cold, slashing)
        match Parser::enclosed(s, '(', ')') {
            None => HashMap::default(),
            Some(traits) => traits
                .split("; ")
                .map(|item| item.split_once(" to ").unwrap())
                .map(|(k, v)| {
                    (
                        k.to_string(),
                        v.split(", ").map(|s| s.to_string()).collect(),
                    )
                })
                .collect(),
        }
    }

    fn boost(&self, kind: Kind, boost: i64) -> Self {
        let mut army = self.clone();
        if army.kind == kind {
            army.damage += boost
        }
        army
    }

    fn dead(&self) -> bool {
        self.units <= 0
    }

    fn power(&self) -> i64 {
        self.units * self.damage
    }

    fn calculate_damage(&self, o: &Self) -> i64 {
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

    fn to_target(&self, o: &Self) -> (i64, i64, i64) {
        (self.calculate_damage(o), o.power(), o.initiative)
    }

    fn hit(&mut self, damage: i64) {
        self.units -= damage / self.hp;
    }
}

#[derive(Debug)]
struct Battle {
    armies: Vec<Army>,
}

impl Battle {
    fn new(groups: &[Vec<String>]) -> Self {
        let mut armies = Vec::default();
        for group in groups[0].iter().skip(1) {
            armies.push(Army::new(armies.len(), Kind::Immune, group));
        }
        for group in groups[1].iter().skip(1) {
            armies.push(Army::new(armies.len(), Kind::Infection, group));
        }
        Self { armies }
    }

    fn boost_immunity(&self, boost: i64) -> Self {
        let armies = self
            .armies
            .iter()
            .map(|army| army.boost(Kind::Immune, boost))
            .collect();
        Self { armies }
    }

    fn simulate(&mut self) {
        let (mut previous, mut current) = (-1, 0);
        while !self.armies.is_empty() && previous != current {
            self.round();
            (previous, current) = (current, self.units());
        }
    }

    fn round(&mut self) {
        self.armies.sort_by_key(|army| Reverse(army.to_choose()));
        let assignments = self.assign_targets();
        for (_, army_id, target_id) in assignments.into_iter() {
            let (army, target) = (self.with_id(army_id), self.with_id(target_id));
            if army.dead() {
                continue;
            }
            let damage = army.calculate_damage(target);
            self.armies
                .iter_mut()
                .filter(|a| a.id == target_id)
                .for_each(|a| a.hit(damage));
        }
        self.armies.retain(|army| !army.dead());
    }

    fn assign_targets(&self) -> Vec<(i64, usize, usize)> {
        let mut result = Vec::default();
        let mut used = HashSet::default();
        for army in self.armies.iter() {
            match self.get_target(army, &used) {
                None => (),
                Some(target) => {
                    result.push((army.initiative, army.id, target.id));
                    used.insert(target.id);
                }
            }
        }
        result.sort_by_key(|(initiative, _, _)| Reverse(*initiative));
        result
    }

    fn get_target(&self, army: &Army, used: &HashSet<usize>) -> Option<&Army> {
        self.with_kind(army.kind.enemy())
            .into_iter()
            .filter(|target| !used.contains(&target.id))
            .filter(|target| army.calculate_damage(target) > 0)
            .max_by_key(|target| army.to_target(target))
    }

    fn with_kind(&self, kind: Kind) -> Vec<&Army> {
        self.armies.iter().filter(|a| a.kind == kind).collect()
    }

    fn with_id(&self, id: usize) -> &Army {
        self.armies.iter().find(|a| a.id == id).unwrap()
    }

    fn immune_won(&self) -> bool {
        let immune = self.with_kind(Kind::Immune);
        let infection = self.with_kind(Kind::Infection);
        !immune.is_empty() && infection.is_empty()
    }

    fn units(&self) -> i64 {
        self.armies.iter().map(|army| army.units).sum()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().groups();
    let battle = Battle::new(&groups);
    answer::part1(16086, part_1(&battle));
    answer::part2(3957, part_2(&battle).unwrap());
}

fn part_1(battle: &Battle) -> i64 {
    let mut battle = battle.boost_immunity(0);
    battle.simulate();
    battle.units()
}

fn part_2(battle: &Battle) -> Option<i64> {
    (1..).find_map(|boost| {
        let mut battle = battle.boost_immunity(boost);
        battle.simulate();
        if battle.immune_won() {
            Some(battle.units())
        } else {
            None
        }
    })
}
