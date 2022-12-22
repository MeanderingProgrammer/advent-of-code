use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::Point;
use aoc_lib::reader;

#[derive(Debug)]
enum Instruction {
    Move(i64),
    Left,
    Right,
}

#[derive(Debug)]
struct State {
    position: Point,
    direction: Point,
}

fn main() {
    let (grid, instructions) = get_input();
    let state = get_start_state(&grid);

    println!("{}", grid.as_string("x", 0));
    println!("{:?}", instructions);
    println!("{:?}", state);

    //answer::part1(v1, s1);
    //answer::part2(v2, s2);
}

fn get_start_state(grid: &Grid<char>) -> State {
    let x = grid.points().iter()
        .filter(|point| point.y() == 0)
        .map(|point| point.x())
        .min()
        .unwrap();
    State {
        position: Point::new_2d(x, 0),
        direction: Point::new_2d(1, 0),
    }
}

fn get_input() -> (Grid<char>, Vec<Instruction>) {
    let data = reader::read_group_lines();

    let grid = Grid::from_lines(data[0].clone(), |ch| {
        if ch == ' ' { None } else { Some(ch) }
    });

    let instructions: Vec<Instruction> = data[1][0].clone()
        .replace("L", ",L,")
        .replace("R", ",R,")
        .split(",")
        .map(|part| {
            match part {
                "L" => Instruction::Left,
                "R" => Instruction::Right,
                amount => Instruction::Move(amount.parse::<i64>().unwrap()),
            }
        })
        .collect();

    (grid, instructions)
}
