use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::line::Line2d;
use aoc_lib::point::Point;
use aoc_lib::reader;

const STARTING_POINT: (i64, i64) = (500, 0);

fn main() {
    answer::part1(610, fill_with_sand(false));
    answer::part2(27194, fill_with_sand(true));
}

fn fill_with_sand(with_floor: bool) -> i64 {
    let mut grid = get_grid();
    let bounds = grid.bounds(0);
    let max_height = bounds.upper().y() + if with_floor { 1 } else { 0 };

    let mut amount_sand = 0;
    let mut landed = true;
    let start = starting_point();

    while landed {
        let (grain_position, fell_through) = drop_grain(&grid, max_height);
        if !with_floor && fell_through {
            landed = false;
        } else {
            grid.add(grain_position.clone(), 'O');
            amount_sand += 1;
        }
        if with_floor && grain_position == start {
            landed = false;
        }
    }

    amount_sand
}

fn drop_grain(grid: &Grid<char>, max_height: i64) -> (Point, bool) {
    let mut can_fall = true;
    let mut fell_through = false;

    let mut grain = starting_point();
    while can_fall && !fell_through {
        let options = vec![
            (0, 1),
            (-1, 1),
            (1, 1),
        ];
        
        let next = options.into_iter()
            .find(|(x, y)| {
                let result = grain.add_x(*x).add_y(*y);
                !grid.contains(&result)
            });

        match next {
            None => can_fall = false,
            Some((x, y)) => grain = grain.add_x(x).add_y(y),
        }

        if grain.y() >= max_height {
            fell_through = true;
        }
    }
    (grain, fell_through)
}

fn get_grid() -> Grid<char> {
    let rock_formations: Vec<Vec<Point>> = reader::read(|line| {
        line.to_string().split(" -> ")
            .map(|point| match point.split_once(",") {
                Some((x, y)) => Point::new_2d(
                    x.parse::<i64>().unwrap(), 
                    y.parse::<i64>().unwrap(),
                ),
                None => panic!(),
            })
            .collect()
    });

    let mut grid: Grid<char> = Grid::new();
    grid.add(starting_point(), '+');
    rock_formations.iter()
        .flat_map(|rock_formation| (1..rock_formation.len())
            .map(|i| Line2d::new(
                rock_formation[i - 1].clone(), 
                rock_formation[i].clone(),
            ))
        )
        .flat_map(|line| line.as_points().into_iter())
        .for_each(|point| grid.add(point.clone(), '#'));
    grid
}

fn starting_point() -> Point {
    Point::new_2d(STARTING_POINT.0, STARTING_POINT.1)
}
