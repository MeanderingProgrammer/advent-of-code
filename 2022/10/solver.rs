use aoc_lib::answer;
use aoc_lib::reader;

fn main() {
    let instructions = reader::read_lines();

    let mut x = 1;
    let mut cycles: Vec<i64> = Vec::new();

    for instruction in instructions {
        let parts: Vec<&str> = instruction.split(" ").collect();
        match parts[0] {
            "noop" => cycles.push(x),
            "addx" => {
                cycles.push(x);
                cycles.push(x);
                x += parts[1].parse::<i64>().unwrap();
            }
            _ => unreachable!(),
        };
    }

    answer::part1(
        11780,
        [20, 60, 100, 140, 180, 220]
            .iter()
            .map(|cycle| *cycle as i64 * cycles[cycle - 1])
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
        get_crt_row(&cycles).join("\n"),
    );
}

fn get_crt_row(cycles: &[i64]) -> Vec<String> {
    let mut rows = Vec::new();
    rows.push("".to_string());
    for row in 0..6 {
        let mut line = "".to_string();
        for column in 0..40 {
            let index = row * 40 + column;
            let position = cycles[index];
            line += if column as i64 <= position + 1 && column as i64 >= position - 1 {
                "#"
            } else {
                "."
            };
        }
        rows.push(line);
    }
    rows
}
