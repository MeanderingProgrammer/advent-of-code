use aoc_lib::answer;
use aoc_lib::reader;
use md5;

struct Password {
    state: [Option<char>; 8],
}

impl Password {
    fn new() -> Self {
        Self { state: [None; 8] }
    }

    fn done(&self) -> bool {
        !self.state.iter().any(|ch| ch.is_none())
    }

    fn next_index(&self) -> usize {
        self.state.iter().filter(|ch| ch.is_some()).count()
    }

    fn can_set(&self, index: usize) -> bool {
        index < self.state.len() && self.state[index].is_none()
    }

    fn set(&mut self, index: usize, value: Option<char>) {
        self.state[index] = value;
    }

    fn to_string(&self) -> String {
        self.state.iter()
            .map(|ch| ch.unwrap())
            .collect()
    }
}

trait PasswordPopulator {
    fn populate(&self, password: &mut Password, hash_chars: &mut impl Iterator<Item = char>);
}

struct Part1;

impl PasswordPopulator for Part1 {
    fn populate(&self, password: &mut Password, hash_chars: &mut impl Iterator<Item = char>) {
        let index = password.next_index();
        password.set(index, hash_chars.next());
    }
}

struct Part2;

impl PasswordPopulator for Part2 {
    fn populate(&self, password: &mut Password, hash_chars: &mut impl Iterator<Item = char>) {
        let raw_index = hash_chars.next().unwrap().to_digit(10);
        if raw_index.is_some() {
            let index = usize::try_from(raw_index.unwrap()).unwrap();
            if password.can_set(index) {
                password.set(index, hash_chars.next());
            }
        }
    }
}

fn main() {
    let lines = reader::read_lines();
    let door_id = &lines[0];

    answer::part1("d4cd2ee1", &get_password(door_id, Part1));
    answer::part2("f2c730e5", &get_password(door_id, Part2));
}

fn get_password(door_id: &str, populator: impl PasswordPopulator) -> String {
    let mut password = Password::new();
    let mut i = 0;

    while !password.done() {
        let hash = get_hash(door_id, i);
        if &hash[0..5] == "00000" {
            let mut hash_chars = hash.chars().skip(5);
            populator.populate(&mut password, &mut hash_chars);
        }
        i += 1;
    }

    password.to_string()
}

fn get_hash(door_id: &str, i: i64) -> String {
    format!("{:x}", md5::compute(format!("{}{}", door_id, i)))
}
