use aoc_lib::answer;
use aoc_lib::reader;
use priority_queue::PriorityQueue;

#[derive(Debug)]
struct RobotInstruction {
    material: usize,
    requirements: [i64; 3],
}

#[derive(Debug)]
struct Blueprint {
    id: i64,
    instructions: Vec<RobotInstruction>,
    max_values: [i64; 3],
}

impl Blueprint {
    fn new(id: i64, instructions: Vec<RobotInstruction>) -> Self {
        let mut max_values = [0, 0, 0];

        instructions.iter()
            .flat_map(|instruction| instruction.requirements.iter().enumerate())
            .for_each(|(material, &needed)| max_values[material] = max_values[material].max(needed));

        Self { id, instructions, max_values }
    }

    fn exceeds_max(&self, state: &State) -> bool {
        self.max_values.iter().enumerate()
            .any(|(material, &max_value)| state.robots[material] > max_value)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct State {
    time_left: i64,
    robots: [i64; 4],
    materials: [i64; 4],
}

impl State {
    fn new(runtime: i64) -> Self {
        State {
            time_left: runtime,
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

    fn can_build(&self, instruction: &RobotInstruction) -> bool {
        instruction.requirements.iter().enumerate()
            .filter(|(_, &needed)| needed > 0)
            .all(|(material, &needed)| self.materials[material] >= needed)
    }

    fn collect(&mut self, blueprint: &Blueprint) {
        self.time_left -= 1;
        for (material, quantity) in self.robots.iter().enumerate() {
            self.materials[material] += quantity;
            if material < 3 {
                // By capping materials to twice the maximum we make a lot of very similar states look
                // identical and allow them to be pruned.
                // For example having 100 ore vs 102 ore makes no difference everything else being equal.
                self.materials[material] = self.materials[material].min(blueprint.max_values[material] * 2);
            }
        }
    }

    fn build_robot(&self, instruction: &RobotInstruction, blueprint: &Blueprint) -> Self {
        let mut next_state = self.remove_materials(instruction);
        next_state.collect(blueprint);
        next_state.robots[instruction.material] += 1;
        next_state
    }

    fn remove_materials(&self, instruction: &RobotInstruction) -> Self {
        let mut updated_materials = self.materials.clone();
        instruction.requirements.iter().enumerate()
            .for_each(|(material, needed)| {
                updated_materials[material] -= needed;
            });
        
        Self {
            time_left: self.time_left,
            robots: self.robots.clone(),
            materials: updated_materials,
        }
    }
}

fn main() {
    let blueprints = get_blueprints();
    answer::part1(1599, blueprints.iter().map(|blueprint| simulate(blueprint, 24) * blueprint.id).sum());
    answer::part2(14112, blueprints.iter().take(3).map(|blueprint| simulate(blueprint, 32)).product());
}

fn simulate(blueprint: &Blueprint, runtime: i64) -> i64 {
    let mut q = PriorityQueue::new();
    q.push(State::new(runtime), (runtime, 0));

    let mut max_geodes_seen = 0;

    while !q.is_empty() {
        let (state, (time_left, num_geods)) = q.pop().unwrap();
        max_geodes_seen = max_geodes_seen.max(num_geods);

        if time_left == 0 {
            break;
        }

        // If we build more of a specific type of robot then we could ever use
        // If clay robots cost 10 ore, then having more than 10 ore robots will create wasted resources
        if blueprint.exceeds_max(&state) {
            continue;
        }

        // Prune if there's no way this state can catch up to something we've already seen
        let max_additional_geodes = (time_left * (time_left + 1)) / 2;
        if num_geods + (state.geode_robots() * time_left) + max_additional_geodes <= max_geodes_seen {
            continue;
        }

        for instruction in &blueprint.instructions {
            if state.can_build(instruction) {
                let next_state = state.build_robot(instruction, blueprint);
                let num_geods = next_state.geodes();
                q.push_increase(next_state, (time_left - 1, num_geods));
            }
        }

        let mut next_state = state.clone();
        next_state.collect(blueprint);
        let num_geods = next_state.geodes();
        q.push_increase(next_state, (time_left - 1, num_geods));
    }

    max_geodes_seen
}

fn get_blueprints() -> Vec<Blueprint> {
    reader::read(|line| {
        let (blueprint_id_data, robots_data) = line.split_once(": ").unwrap();
        let (_, blueprint_id) = blueprint_id_data.split_once(" ").unwrap();
        Blueprint::new(
            blueprint_id.parse::<i64>().unwrap(), 
            robots_data.split(".")
                .map(|value| value.trim())
                .filter(|value| value.len() > 0)
                .map(|value| parse_robot_instruction(value))
                .collect(),
        )
    })
}

fn parse_robot_instruction(line: &str) -> RobotInstruction {
    let parts: Vec<&str> = line.split(" ").collect();
    RobotInstruction {
        material: parse_material(parts[1]),
        requirements: match parts.len() {
            6 => {
                let mut value = [0, 0, 0];
                value[parse_material(parts[5])] = parts[4].parse::<i64>().unwrap();
                value
            },
            9 => {
                let mut value = [0, 0, 0];
                value[parse_material(parts[5])] = parts[4].parse::<i64>().unwrap();
                value[parse_material(parts[8])] = parts[7].parse::<i64>().unwrap();
                value
            },
            _ => panic!("Unhandled length of requirements"),
        },
    }
}

fn parse_material(value: &str) -> usize {
    match value {
        "ore" => 0,
        "clay" => 1,
        "obsidian" => 2,
        "geode" => 3,
        _ => panic!("Unhandled material type"),
    }
}
