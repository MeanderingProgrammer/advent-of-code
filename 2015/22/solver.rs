use aoc::{answer, Dijkstra, Reader};
use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Stats {
    hp: u16,
    attack: u16,
    armor: u16,
}

impl Stats {
    fn new(hp: u16, attack: u16, armor: u16) -> Self {
        Self { hp, attack, armor }
    }

    fn dead(&self) -> bool {
        self.hp == 0
    }

    fn plus(&self, rhs: &Stats) -> Stats {
        Stats::new(
            self.hp + rhs.hp,
            self.attack + rhs.attack,
            self.armor + rhs.armor,
        )
    }

    fn minus(&self, rhs: &Stats) -> Stats {
        Stats::new(
            self.hp.saturating_sub(rhs.hp),
            self.attack.saturating_sub(rhs.attack),
            self.armor.saturating_sub(rhs.armor),
        )
    }
}

#[derive(Debug)]
enum Variant {
    Boost,
    Damage,
    Heal,
    Transfer,
}

#[derive(Debug)]
struct Effect {
    variant: Variant,
    amount: Stats,
}

impl Effect {
    fn add(&self, player: &Stats) -> Stats {
        match self.variant {
            Variant::Boost => player.plus(&self.amount),
            _ => player.clone(),
        }
    }

    fn remove(&self, player: &Stats) -> Stats {
        match self.variant {
            Variant::Boost => player.minus(&self.amount),
            _ => player.clone(),
        }
    }

    fn player(&self, player: &Stats) -> Stats {
        match self.variant {
            Variant::Heal | Variant::Transfer => player.plus(&self.amount),
            _ => player.clone(),
        }
    }

    fn enemy(&self, enemy: &Stats) -> Stats {
        match self.variant {
            Variant::Damage | Variant::Transfer => enemy.minus(&self.amount),
            _ => enemy.clone(),
        }
    }
}

#[derive(Debug, Clone, PartialOrd, Ord, PartialEq, Eq, Hash)]
enum Spell {
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
}

impl Spell {
    fn values() -> &'static [Self] {
        &[
            Self::MagicMissile,
            Self::Drain,
            Self::Shield,
            Self::Poison,
            Self::Recharge,
        ]
    }

    fn cost(&self) -> u16 {
        match self {
            Self::MagicMissile => 53,
            Self::Drain => 73,
            Self::Shield => 113,
            Self::Poison => 173,
            Self::Recharge => 229,
        }
    }

    fn turns(&self) -> usize {
        match self {
            Self::MagicMissile | Self::Drain => 1,
            Self::Shield | Self::Poison => 6,
            Self::Recharge => 5,
        }
    }

    fn effect(&self) -> Effect {
        match self {
            Self::MagicMissile => Effect {
                variant: Variant::Damage,
                amount: Stats::new(4, 0, 0),
            },
            Self::Drain => Effect {
                variant: Variant::Transfer,
                amount: Stats::new(2, 0, 0),
            },
            Self::Shield => Effect {
                variant: Variant::Boost,
                amount: Stats::new(0, 0, 7),
            },
            Self::Poison => Effect {
                variant: Variant::Damage,
                amount: Stats::new(3, 0, 0),
            },
            Self::Recharge => Effect {
                variant: Variant::Heal,
                amount: Stats::new(0, 101, 0),
            },
        }
    }
}

#[derive(Debug, Clone, PartialOrd, Ord, PartialEq, Eq, Hash)]
struct Active {
    spell: Spell,
    turns: usize,
}

impl Active {
    fn new(spell: &Spell) -> Self {
        Self {
            spell: spell.clone(),
            turns: spell.turns(),
        }
    }

    fn next(&self) -> Self {
        Self {
            spell: self.spell.clone(),
            turns: self.turns - 1,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Game {
    player: Stats,
    enemy: Stats,
    damage: Stats,
    active: BTreeSet<Active>,
}

impl Game {
    fn neighbors(&self) -> impl Iterator<Item = (Self, u16)> + '_ {
        Spell::values()
            .iter()
            .filter(|spell| self.can_perform(spell))
            .map(|spell| {
                let mut game = self.clone();
                game.apply(spell);
                (game, spell.cost())
            })
    }

    fn can_perform(&self, spell: &Spell) -> bool {
        if self.player.dead() || self.player.attack < spell.cost() {
            false
        } else {
            !self
                .active
                .iter()
                .any(|active| &active.spell == spell && active.turns > 1)
        }
    }

    fn apply(&mut self, spell: &Spell) {
        self.player = self.player.minus(&self.damage);
        self.active = self.run_spells();

        self.player = self.player.minus(&Stats::new(0, spell.cost(), 0));
        self.player = spell.effect().add(&self.player);
        self.active.insert(Active::new(spell));

        self.player = self.player.minus(&self.damage);
        self.active = self.run_spells();
        self.player = self.player.minus(&self.attack());
    }

    fn run_spells(&mut self) -> BTreeSet<Active> {
        self.active
            .iter()
            .flat_map(|active| {
                let effect = active.spell.effect();
                self.player = effect.player(&self.player);
                self.enemy = effect.enemy(&self.enemy);
                if active.turns == 1 {
                    self.player = effect.remove(&self.player);
                    None
                } else {
                    Some(active.next())
                }
            })
            .collect()
    }

    fn attack(&self) -> Stats {
        Stats::new(1.max(self.enemy.attack - self.player.armor), 0, 0)
    }
}

#[derive(Debug)]
struct Settings {
    hp: u16,
    attack: u16,
}

impl Settings {
    fn new(lines: &[String]) -> Self {
        Self {
            hp: Self::second(&lines[0]),
            attack: Self::second(&lines[1]),
        }
    }

    fn second(s: &str) -> u16 {
        s.split_once(": ").unwrap().1.parse().unwrap()
    }

    fn game(&self, damage: u16) -> Game {
        Game {
            player: Stats::new(50, 500, 0),
            enemy: Stats::new(self.hp, self.attack, 0),
            damage: Stats::new(damage, 0, 0),
            active: BTreeSet::default(),
        }
    }
}

impl Dijkstra for Settings {
    type T = Game;
    type W = u16;

    fn done(&self, node: &Self::T) -> bool {
        node.enemy.dead()
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        node.neighbors()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let settings = Settings::new(&lines);
    answer::part1(1269, settings.run(settings.game(0)).unwrap());
    answer::part2(1309, settings.run(settings.game(1)).unwrap());
}
