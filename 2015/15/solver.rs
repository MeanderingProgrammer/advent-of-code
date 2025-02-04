use aoc::{answer, Parser, Reader};
use std::str::FromStr;

#[derive(Debug, Default)]
struct Ingredient {
    capacity: i64,
    durability: i64,
    flavor: i64,
    texture: i64,
    calories: i64,
}

impl FromStr for Ingredient {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let [capacity, durability, flavor, texture, calories] = Parser::values(s, " ").unwrap();
        Ok(Self {
            capacity,
            durability,
            flavor,
            texture,
            calories,
        })
    }
}

impl Ingredient {
    fn score(&self) -> i64 {
        self.capacity.max(0) * self.durability.max(0) * self.flavor.max(0) * self.texture.max(0)
    }

    fn mul(&self, rhs: usize) -> Self {
        Self {
            capacity: self.capacity * (rhs as i64),
            durability: self.durability * (rhs as i64),
            flavor: self.flavor * (rhs as i64),
            texture: self.texture * (rhs as i64),
            calories: self.calories * (rhs as i64),
        }
    }

    fn add(&mut self, rhs: &Self) {
        self.capacity += rhs.capacity;
        self.durability += rhs.durability;
        self.flavor += rhs.flavor;
        self.texture += rhs.texture;
        self.calories += rhs.calories;
    }
}

#[derive(Debug)]
struct Recipe {
    ingredients: Vec<Ingredient>,
    teaspoons: usize,
    target: i64,
}

impl Recipe {
    fn best_scores(&self) -> (i64, i64) {
        let mut part1 = 0;
        let mut part2 = 0;
        for a in 0..=self.teaspoons {
            for b in 0..=(self.teaspoons - a) {
                for c in 0..=(self.teaspoons - a - b) {
                    let d = self.teaspoons - a - b - c;
                    let properties = self.get_values(vec![a, b, c, d]);
                    part1 = part1.max(properties.score());
                    part2 = part2.max(if self.target == properties.calories {
                        properties.score()
                    } else {
                        0
                    });
                }
            }
        }
        (part1, part2)
    }

    fn get_values(&self, proportion: Vec<usize>) -> Ingredient {
        let mut result = Ingredient::default();
        for (ingredient, amount) in self.ingredients.iter().zip(proportion.into_iter()) {
            result.add(&ingredient.mul(amount));
        }
        result
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let ingredients = Reader::default().read_from_str();
    assert_eq!(ingredients.len(), 4);
    let recipe = Recipe {
        ingredients,
        teaspoons: 100,
        target: 500,
    };
    let (part1, part2) = recipe.best_scores();
    answer::part1(18965440, part1);
    answer::part2(15862900, part2);
}
