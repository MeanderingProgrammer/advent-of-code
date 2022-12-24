//use aoc_lib::answer;
use aoc_lib::grid::Grid;
//use aoc_lib::point::Point;
use aoc_lib::reader;

/*
#[derive(Debug)]
struct Cube {
    faces: [Grid<char>; 6],
}

#[derive(Debug)]
enum Direction {
    Right,
    Down,
    Left,
    Up,
}
*/

#[derive(Debug)]
enum Instruction {
    Move(i64),
    Left,
    Right,
}

fn main() {
    //let lines = reader::read_lines();
    //println!("{:?}", lines);
    get_input();
    //answer::part1(3590, simulate(false));
    //answer::part2(3590, simulate(true));
}

fn get_input() -> (Grid<char>, Vec<Instruction>) {
    let data = reader::read_group_lines();
    parse_cube(&data[0]);
    (
        Grid::new(), 
        parse_instructions(&data[1][0]),
    )
}

fn parse_cube(grid_lines: &Vec<String>) {
    let rows = grid_lines.len();
    let cols = grid_lines.iter()
        .map(|line| line.len())
        .max().unwrap();
    let side_length = rows.min(cols) / 3;

    /*
    let face_index = 0;
    let faces: [Grid<char>; 6];
    
    let face_ordering: [(usize, usize); 6] = [
        (0, 0),
        (1, 2),
        (4, 1),
        (3, 0),
        (5, 0),
        (2, 0),
    ];
    */

    for row_index in 0..(rows/side_length) {
        for column_index in 0..(cols/side_length) {
            let (row, col) = (row_index * side_length, column_index * side_length);
            let line = &grid_lines[row];
            if col < line.len() && &line[col..col+1] != " " {
                let face = parse_face(grid_lines, row, col, side_length);
                println!("REGULAR");
                println!("{}", face);
                println!("ROTATED");
                println!("{}", face.rotate_cw());
                println!("");
            }
        }
    }
}

fn parse_face(grid_lines: &Vec<String>, row: usize, col: usize, side_length: usize) -> Grid<char> {
    let face_lines: Vec<String> = (row..row+side_length)
        .map(|line_number| &grid_lines[line_number])
        .map(|current| &current[col..col+side_length])
        .map(|current| current.to_string())
        .collect();
    Grid::from_lines(face_lines, |ch| Some(ch))
}

fn parse_instructions(line: &str) -> Vec<Instruction> {
    line.replace("L", ",L,")
        .replace("R", ",R,")
        .split(",")
        .map(|part| {
            match part {
                "L" => Instruction::Left,
                "R" => Instruction::Right,
                amount => Instruction::Move(amount.parse::<i64>().unwrap()),
            }
        })
        .collect()
}
