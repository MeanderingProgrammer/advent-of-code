use aoc::int_code::{Bus, Computer};
use aoc::{Direction, HashMap, HashSet, Iter, Reader, answer};
use std::collections::VecDeque;
use std::str::FromStr;

const BAD_ITEMS: [&str; 5] = [
    "giant electromagnet",
    "molten lava",
    "photons",
    "escape pod",
    "infinite loop",
];

#[derive(Debug, Default)]
struct View {
    name: String,
    directions: Vec<Direction>,
    items: Vec<String>,
}

impl FromStr for View {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut view = View::default();
        for group in s.split("\n\n") {
            let values: Vec<&str> = group.split('\n').filter(|s| !s.is_empty()).collect();
            if values.is_empty() {
                continue;
            }
            if values[0].starts_with("==") {
                view.name = values[0][3..values[0].len() - 3].to_string();
            } else if values[0] == "Doors here lead:" {
                let directions = values.iter().skip(1).map(|s| Direction::from_str(&s[2..]));
                directions.for_each(|direction| view.directions.push(direction.unwrap()));
            } else if values[0] == "Items here:" {
                let items = values.iter().skip(1).map(|s| s[2..].to_string());
                items.for_each(|item| view.items.push(item));
            }
        }
        Ok(view)
    }
}

#[derive(Debug, Default)]
struct Graph {
    graph: HashMap<String, HashSet<Direction>>,
}

impl Graph {
    fn node(&mut self, name: &str) -> &mut HashSet<Direction> {
        self.graph.entry(name.to_string()).or_default()
    }

    fn unexplored(&self, name: &str, directions: &[Direction]) -> Option<Direction> {
        let explored = &self.graph[name];
        directions
            .iter()
            .find(|dir| !explored.contains(dir))
            .cloned()
    }
}

#[derive(Debug, Default)]
struct Bag {
    items: Vec<String>,
    index: usize,
    combinations: Option<Vec<Vec<String>>>,
}

impl Bag {
    fn add(&mut self, item: &str) {
        self.items.push(item.to_string());
    }

    fn inventory(&mut self) -> Vec<String> {
        if self.index == 0 {
            self.items.clone()
        } else {
            self.nth(self.index - 1)
        }
    }

    fn next(&mut self) -> Vec<String> {
        self.index += 1;
        self.nth(self.index - 1)
    }

    fn nth(&mut self, n: usize) -> Vec<String> {
        match &self.combinations {
            None => {
                let combinations: Vec<Vec<String>> = (1..=self.items.len())
                    .flat_map(|size| self.items.iter().cloned().combinations(size))
                    .collect();
                self.combinations = Some(combinations);
                self.next()
            }
            Some(combinations) => combinations[n].clone(),
        }
    }
}

#[derive(Debug, Default)]
enum State {
    #[default]
    Exploring,
    Solving,
}

#[derive(Debug, Default)]
struct DroidBus {
    instruction: String,
    commands: VecDeque<char>,
    state: State,
    grid: Graph,
    previous: Option<(String, Direction)>,
    history: Vec<Direction>,
    path: Vec<Direction>,
    bag: Bag,
}

impl DroidBus {
    fn explored(&mut self) -> bool {
        let view = View::from_str(&self.instruction).unwrap();
        self.instruction = String::default();

        let location = view.name;
        match &self.previous {
            None => {
                self.grid.node(&location);
            }
            Some(prev) => {
                self.grid.node(&prev.0).insert(prev.1.clone());
                self.grid.node(&location).insert(prev.1.opposite());
            }
        }

        view.items
            .iter()
            .filter(|item| !BAD_ITEMS.contains(&item.as_str()))
            .for_each(|item| {
                self.bag.add(item);
                self.add_command(&format!("take {item}"));
            });

        let directions = if location == "Security Checkpoint" {
            self.path = self.history.clone();
            // Remove direction which takes us to analyzer, for initial traversal
            view.directions.into_iter().skip(1).collect()
        } else {
            view.directions
        };

        if let Some(command) = self.grid.unexplored(&location, &directions) {
            self.history.push(command.clone());
            self.add_direction(&command);
            self.previous = Some((location, command));
            false
        } else if let Some(command) = self.history.pop() {
            let command = command.opposite();
            self.add_direction(&command);
            self.previous = Some((location, command));
            false
        } else {
            true
        }
    }

    fn next_solution(&mut self) {
        self.bag.inventory().iter().for_each(|item| {
            self.add_command(&format!("drop {item}"));
        });
        self.bag.next().iter().for_each(|item| {
            self.add_command(&format!("take {item}"));
        });
        self.add_direction(&Direction::Down);
    }

    fn add_direction(&mut self, direction: &Direction) {
        let command = match direction {
            Direction::Up => "north",
            Direction::Down => "south",
            Direction::Right => "east",
            Direction::Left => "west",
        };
        self.add_command(command);
    }

    fn add_command(&mut self, command: &str) {
        self.commands.append(&mut command.chars().collect());
        self.commands.push_back('\n');
    }

    fn get_key(&self) -> i64 {
        let lines = self.instruction.split('\n').filter(|s| !s.is_empty());
        let last_line = lines.last().unwrap().split_whitespace().collect::<Vec<_>>();
        last_line[last_line.len() - 8].parse().unwrap()
    }
}

impl Bus for DroidBus {
    fn active(&self) -> bool {
        true
    }

    fn add_output(&mut self, value: i64) {
        self.instruction.push(char::from_u32(value as u32).unwrap());
    }

    fn get_input(&mut self) -> i64 {
        if let Some(command) = self.commands.pop_front() {
            command as i64
        } else {
            match self.state {
                State::Exploring => {
                    if self.explored() {
                        let path = self.path.clone();
                        path.iter()
                            .for_each(|direction| self.add_direction(direction));
                        self.add_direction(&Direction::Down);
                        self.state = State::Solving;
                    }
                }
                State::Solving => self.next_solution(),
            }
            self.get_input()
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    let mut computer: Computer<DroidBus> = Computer::default(&memory);
    computer.run();
    answer::part1(2622472, computer.bus.get_key());
}
