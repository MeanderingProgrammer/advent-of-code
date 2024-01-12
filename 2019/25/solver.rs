use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::point::Direction;
use aoc_lib::reader;
use fxhash::{FxHashMap, FxHashSet};
use itertools::{Combinations, Itertools};
use std::collections::VecDeque;
use std::str::FromStr;
use std::vec::IntoIter;

const BAD_ITEMS: [&str; 5] = [
    "giant electromagnet",
    "molten lava",
    "photons",
    "escape pod",
    "infinite loop",
];

#[derive(Debug)]
struct View {
    name: String,
    directions: Vec<Direction>,
    items: Vec<String>,
}

impl FromStr for View {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut view = View {
            name: String::new(),
            directions: Vec::new(),
            items: Vec::new(),
        };
        for group in s.split("\n\n") {
            let values: Vec<&str> = group.split("\n").filter(|s| !s.is_empty()).collect();
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

#[derive(Debug)]
struct Graph {
    graph: FxHashMap<String, FxHashSet<Direction>>,
}

impl Graph {
    fn add_node(&mut self, name: &str) {
        if !self.graph.contains_key(name) {
            self.graph.insert(name.to_string(), FxHashSet::default());
        }
    }

    fn add_edge(&mut self, start: &str, direction: &Direction, end: &str) {
        let from_start = self.graph.get_mut(start).unwrap();
        from_start.insert(direction.clone());
        let from_end = self.graph.get_mut(end).unwrap();
        from_end.insert(direction.opposite());
    }

    fn get_unexplored(&self, name: &str, directions: &Vec<Direction>) -> Option<Direction> {
        let explored = &self.graph[name];
        directions
            .iter()
            .filter(|dir| !explored.contains(dir))
            .next()
            .map(|direction| direction.clone())
    }
}

#[derive(Debug)]
struct ItemBag {
    items: Vec<String>,
    index: usize,
    current: Option<Combinations<IntoIter<String>>>,
}

impl ItemBag {
    fn new() -> Self {
        Self {
            items: Vec::new(),
            index: 1,
            current: None,
        }
    }

    fn add(&mut self, item: &str) {
        self.items.push(item.to_string());
    }
}

impl Iterator for ItemBag {
    type Item = Vec<String>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current.is_none() {
            self.current = Some(self.items.clone().into_iter().combinations(self.index));
        }
        let mut next_value = self.current.as_mut().unwrap().next();
        if next_value.is_none() {
            self.index += 1;
            self.current = Some(self.items.clone().into_iter().combinations(self.index));
            next_value = self.current.as_mut().unwrap().next();
        }
        next_value
    }
}

#[derive(Debug)]
enum State {
    Exploring,
    Solving,
}

#[derive(Debug)]
struct DroidBus {
    instruction: String,
    commands: VecDeque<char>,
    state: State,
    grid: Graph,
    previous: Option<(String, Direction)>,
    history: Vec<Direction>,
    path_to_checkpoint: Vec<Direction>,
    item_bag: ItemBag,
}

impl DroidBus {
    fn new() -> Self {
        Self {
            instruction: String::new(),
            commands: VecDeque::new(),
            state: State::Exploring,
            grid: Graph {
                graph: FxHashMap::default(),
            },
            previous: None,
            history: Vec::new(),
            path_to_checkpoint: Vec::new(),
            item_bag: ItemBag::new(),
        }
    }

    fn continue_exploring(&mut self) -> bool {
        let view = View::from_str(&self.instruction).unwrap();
        self.instruction = String::new();

        let location = view.name;
        self.grid.add_node(&location);
        match &self.previous {
            Some(prev) => self.grid.add_edge(&prev.0, &prev.1, &location),
            None => (),
        }

        view.items
            .iter()
            .filter(|item| !BAD_ITEMS.contains(&item.as_str()))
            .for_each(|item| {
                self.item_bag.add(item);
                self.add_command(&format!("take {item}"));
            });

        let directions = if location == "Security Checkpoint" {
            self.path_to_checkpoint = self.history.clone();
            // Remove direction which takes us to analyzer, for initial traversal
            view.directions.into_iter().skip(1).collect()
        } else {
            view.directions
        };
        let unexplored = self.grid.get_unexplored(&location, &directions);

        if unexplored.is_some() {
            let command = unexplored.unwrap();
            self.history.push(command.clone());
            self.previous = Some((location, command.clone()));
            self.add_direction(command);
            true
        } else if !self.history.is_empty() {
            let command = self.history.pop().unwrap().opposite();
            self.previous = Some((location, command.clone()));
            self.add_direction(command);
            true
        } else {
            false
        }
    }

    fn attempt_solve(&mut self) {
        let items_to_drop = self.item_bag.items.clone();
        items_to_drop.iter().for_each(|item| {
            self.add_command(&format!("drop {item}"));
        });
        self.item_bag.next().unwrap().iter().for_each(|item| {
            self.add_command(&format!("take {item}"));
        });
        self.add_direction(Direction::Down);
    }

    fn add_direction(&mut self, direction: Direction) {
        let command = match direction {
            Direction::Up => "north",
            Direction::Down => "south",
            Direction::Right => "east",
            Direction::Left => "west",
        };
        self.add_command(command);
    }

    fn add_command(&mut self, command: &str) {
        let as_string = command.to_string() + "\n";
        self.commands.append(&mut as_string.chars().collect());
    }

    fn get_key(&self) -> i64 {
        let lines = self.instruction.split("\n").filter(|s| !s.is_empty());
        let last_line = lines.last().unwrap().split_whitespace().collect_vec();
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
        if self.commands.is_empty() {
            match self.state {
                State::Exploring => {
                    if !self.continue_exploring() {
                        let path = self.path_to_checkpoint.clone();
                        path.into_iter()
                            .for_each(|direction| self.add_direction(direction));
                        self.add_direction(Direction::Down);
                        self.state = State::Solving;
                    }
                }
                State::Solving => self.attempt_solve(),
            }
        }
        self.commands.pop_front().unwrap() as i64
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let mut computer = Computer::new(DroidBus::new(), reader::read_csv());
    computer.run();
    answer::part1(2622472, computer.bus.get_key());
}
