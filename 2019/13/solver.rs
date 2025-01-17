use aoc_lib::answer;
use aoc_lib::int_code::{Bus, Computer};
use aoc_lib::reader::Reader;
use fxhash::FxHashMap;

#[derive(Debug, Default)]
struct Game {
    tile_buffer: Vec<i64>,
    tile_freq: FxHashMap<String, i64>,
    tile_x: FxHashMap<String, i64>,
    score: i64,
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
                self.score = value;
            } else {
                let name = match value {
                    0 => "empty",
                    1 => "wall",
                    2 => "block",
                    3 => "horizontal paddle",
                    4 => "ball",
                    _ => panic!("Unknown tile value"),
                };
                *self.tile_freq.entry(name.to_string()).or_insert(0) += 1;
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
    let memory = Reader::default().read_csv();
    answer::part1(363, play_game(&memory, false));
    answer::part2(17159, play_game(&memory, true));
}

fn play_game(memory: &[i64], play_for_free: bool) -> i64 {
    let mut memory = memory.to_vec();
    if play_for_free {
        memory[0] = 2;
    }
    let mut computer: Computer<Game> = Computer::default(&memory);
    computer.run();
    if play_for_free {
        computer.bus.score
    } else {
        *computer.bus.tile_freq.get("block").unwrap()
    }
}
