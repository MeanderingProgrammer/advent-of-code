use aoc_lib::answer;
use aoc_lib::reader;
use std::str::FromStr;

#[derive(Debug)]
enum Instruction {
    Noop,
    Add(i64),
}

impl FromStr for Instruction {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split(" ").collect();
        match parts[0] {
            "noop" => Ok(Self::Noop),
            "addx" => Ok(Self::Add(parts[1].parse().unwrap())),
            _ => Err("Unkown instruction operation".to_string()),
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let instructions = reader::read(|line| line.parse::<Instruction>().unwrap());
    let cycles = get_cycles(instructions);

    answer::part1(
        11780,
        [20, 60, 100, 140, 180, 220]
            .into_iter()
            .map(|cycle| cycle as i64 * cycles[cycle - 1])
            .sum(),
    );
    answer::part2(
        // PZULBAUA
        [
            "",
            "###..####.#..#.#....###...##..#..#..##..",
            "#..#....#.#..#.#....#..#.#..#.#..#.#..#.",
            "#..#...#..#..#.#....###..#..#.#..#.#..#.",
            "###...#...#..#.#....#..#.####.#..#.####.",
            "#....#....#..#.#....#..#.#..#.#..#.#..#.",
            "#....####..##..####.###..#..#..##..#..#.",
        ]
        .join("\n"),
        get_crt(&cycles, 6, 40).join("\n"),
    );
}

fn get_cycles(instructions: Vec<Instruction>) -> Vec<i64> {
    let mut current: i64 = 1;
    let mut cycles: Vec<i64> = Vec::new();
    for instruction in instructions {
        match instruction {
            Instruction::Noop => cycles.push(current),
            Instruction::Add(amount) => {
                cycles.push(current);
                cycles.push(current);
                current += amount;
            }
        };
    }
    cycles
}

fn get_crt(cycles: &Vec<i64>, rows: usize, columns: usize) -> Vec<String> {
    let mut result = Vec::new();
    result.push("".to_string());
    for row in 0..rows {
        let pixels: Vec<String> = (0..columns)
            .map(|column| {
                let index = row * columns + column;
                let position = cycles[index];
                get_pixel(column as i64, position)
            })
            .collect();
        result.push(pixels.join(""));
    }
    result
}

fn get_pixel(column: i64, position: i64) -> String {
    let pixel = if column <= position + 1 && column >= position - 1 {
        "#"
    } else {
        "."
    };
    pixel.to_string()
}
