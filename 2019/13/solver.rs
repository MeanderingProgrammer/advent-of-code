use aoc::int_code::{Bus, Computer};
use aoc::{HashMap, Iter, Reader, answer};

#[derive(Debug, Default)]
struct Game {
    tile_buffer: Vec<i64>,
    tiles: Vec<String>,
    tile_x: HashMap<String, i64>,
    score: usize,
}

impl Bus for Game {
    fn active(&self) -> bool {
        true
    }

    fn get_input(&mut self) -> i64 {
        let diff = self.tile_x["ball"] - self.tile_x["horizontal paddle"];
        1.min(diff.max(-1))
    }

    fn add_output(&mut self, value: i64) {
        self.tile_buffer.push(value);
        if self.tile_buffer.len() == 3 {
            let x = self.tile_buffer[0];
            let y = self.tile_buffer[1];
            let value = self.tile_buffer[2];
            if x == -1 && y == 0 {
                self.score = value as usize;
            } else {
                let name = match value {
                    0 => "empty",
                    1 => "wall",
                    2 => "block",
                    3 => "horizontal paddle",
                    4 => "ball",
                    _ => panic!("Unknown tile value"),
                };
                self.tiles.push(name.to_string());
                self.tile_x.insert(name.to_string(), x);
            }
            self.tile_buffer.clear();
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let memory = Reader::default().csv();
    answer::part1(363, play_game(&memory, false));
    answer::part2(17159, play_game(&memory, true));
}

fn play_game(memory: &[i64], part2: bool) -> usize {
    let mut memory = memory.to_vec();
    if part2 {
        memory[0] = 2;
    }
    let mut computer: Computer<Game> = Computer::default(&memory);
    computer.run();
    if part2 {
        computer.bus.score
    } else {
        let tiles = computer.bus.tiles;
        *tiles.into_iter().counts().get("block").unwrap()
    }
}
