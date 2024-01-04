use aoc_lib::answer;
use aoc_lib::reader;
use priority_queue::PriorityQueue;
use std::str::FromStr;

#[derive(Debug)]
struct Instruction {
    material: usize,
    requirements: [i64; 3],
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        fn parse_material(value: &str) -> usize {
            match value {
                "ore" => 0,
                "clay" => 1,
                "obsidian" => 2,
                "geode" => 3,
                _ => panic!("Unhandled material type"),
            }
        }

        let parts: Vec<&str> = s.split(" ").collect();
        Ok(Self {
            material: parse_material(parts[1]),
            requirements: match parts.len() {
                6 => {
                    let mut value = [0, 0, 0];
                    value[parse_material(parts[5])] = parts[4].parse().unwrap();
                    value
                }
                9 => {
                    let mut value = [0, 0, 0];
                    value[parse_material(parts[5])] = parts[4].parse().unwrap();
                    value[parse_material(parts[8])] = parts[7].parse().unwrap();
                    value
                }
                _ => panic!("Unhandled length of requirements"),
            },
        })
    }
}

#[derive(Debug)]
struct Blueprint {
    id: i64,
    instructions: Vec<Instruction>,
    max_values: [i64; 3],
}

impl FromStr for Blueprint {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (id_data, instruction_data) = s.split_once(": ").unwrap();

        let id: i64 = id_data.split_once(" ").unwrap().1.parse().unwrap();

        let instructions: Vec<Instruction> = instruction_data
            .split(".")
            .map(|value| value.trim())
            .filter(|value| value.len() > 0)
            .map(|value| value.parse().unwrap())
            .collect();

        let mut max_values = [0, 0, 0];
        instructions
            .iter()
            .flat_map(|instruction| instruction.requirements.iter().enumerate())
            .for_each(|(material, &needed)| {
                max_values[material] = max_values[material].max(needed)
            });

        Ok(Self {
            id,
            instructions,
            max_values,
        })
    }
}

impl Blueprint {
    fn simulate(&self, runtime: i64) -> i64 {
        let mut q = PriorityQueue::new();
        q.push(State::new(), (0, runtime));
        let mut max_geodes_seen = 0;
        while !q.is_empty() {
            let (state, (num_geods, time_left)) = q.pop().unwrap();
            max_geodes_seen = max_geodes_seen.max(num_geods);
            if time_left == 0 {
                continue;
            }
            let mut valid_instructions: Vec<Option<&Instruction>> = self
                .instructions
                .iter()
                .filter(|instruction| state.can_build(instruction))
                .map(|instruction| Some(instruction))
                .collect();
            valid_instructions.push(None);
            let next_time_left = time_left - 1;
            for instruction in valid_instructions {
                let mut next_state = state.clone();
                next_state.collect();
                if instruction.is_some() {
                    next_state.build_robot(instruction.unwrap());
                }
                for material in 0..3 {
                    // By capping materials to twice maximum we make similar states look identical allowing them to be pruned.
                    let material_cap = self.max_values[material] * 2;
                    let capped = next_state.materials[material].min(material_cap);
                    next_state.materials[material] = capped;
                }
                // If we build more of a specific type of robot then we could ever use
                // If clay robots cost 10 ore, then having > 10 ore robots adds no value
                if self.exceeds_max(&next_state) {
                    continue;
                }
                // Prune if there's no way this state can catch up to something we've already seen
                if Self::max_geodes(&next_state, next_time_left) <= max_geodes_seen {
                    continue;
                }
                let next_num_geods = next_state.geodes();
                q.push_increase(next_state, (next_num_geods, next_time_left));
            }
        }
        max_geodes_seen
    }

    fn exceeds_max(&self, state: &State) -> bool {
        self.max_values
            .iter()
            .enumerate()
            .any(|(material, &max_value)| state.robots[material] > max_value)
    }

    fn max_geodes(state: &State, time_left: i64) -> i64 {
        let max_additional = (time_left * (time_left + 1)) / 2;
        state.geodes() + (state.geode_robots() * time_left) + max_additional
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    robots: [i64; 4],
    materials: [i64; 4],
}

impl State {
    fn new() -> Self {
        Self {
            robots: [1, 0, 0, 0],
            materials: [0, 0, 0, 0],
        }
    }

    fn geodes(&self) -> i64 {
        self.materials[3]
    }

    fn geode_robots(&self) -> i64 {
        self.robots[3]
    }

    fn can_build(&self, instruction: &Instruction) -> bool {
        instruction
            .requirements
            .iter()
            .enumerate()
            .filter(|(_, &needed)| needed > 0)
            .all(|(material, &needed)| self.materials[material] >= needed)
    }

    fn collect(&mut self) {
        for (material, quantity) in self.robots.iter().enumerate() {
            self.materials[material] += quantity;
        }
    }

    fn build_robot(&mut self, instruction: &Instruction) {
        instruction
            .requirements
            .iter()
            .enumerate()
            .for_each(|(material, needed)| self.materials[material] -= needed);
        self.robots[instruction.material] += 1;
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let bps: Vec<Blueprint> = reader::read(|line| line.parse().unwrap());
    answer::part1(1599, bps.iter().map(|bp| bp.simulate(24) * bp.id).sum());
    answer::part2(
        14112,
        bps.iter().take(3).map(|bp| bp.simulate(32)).product(),
    );
}
