https://github.com/NickyMeuleman/scrapyard/blob/main/advent_of_code/2022/src/day_22.rs

```
#[derive(Debug)]
struct State {
    position: Point,
    direction: Point,
}

impl State {
    fn apply(&mut self, instruction: &Instruction, grid: &Grid<char>, as_cube: bool) {
        match instruction {
            Instruction::Move(amount) => {
                for _ in 0..*amount {
                    let (new_position, next_value) = self.next(grid, as_cube);
                    if next_value == '#' {
                        break;
                    }
                    self.position = new_position;                    
                }
            },
            Instruction::Left => {
                self.direction = self.direction.rotate_cw().rotate_cw().rotate_cw();
            },
            Instruction::Right => {
                self.direction = self.direction.rotate_cw();
            },
        }
    }

    fn next(&self, grid: &Grid<char>, as_cube: bool) -> (Point, char) {
        let (x, y) = (self.direction.x(), self.direction.y());
        let new_position = self.position.add_x(x).add_y(y);
        if grid.contains(&new_position) {
            let value = grid.get(&new_position);
            (new_position, value.clone())
        } else if !as_cube {
            self.next_linear(grid)
        } else {
            self.next_cube(grid)
        }
    }

    fn next_linear(&self, grid: &Grid<char>) -> (Point, char) {
        let (x, y) = (self.direction.x(), self.direction.y());
        let bound = grid.bounds(0);
        let mut search_position = match (x, y) {
            (1, 0) => Point::new_2d(bound.lower().x(), self.position.y()),
            (-1, 0) => Point::new_2d(bound.upper().x(), self.position.y()),
            (0, 1) => Point::new_2d(self.position.x(), bound.lower().y()),
            (0, -1) => Point::new_2d(self.position.x(), bound.upper().y()),
            _ => unreachable!(),
        };
        
        while !grid.contains(&search_position) {
            search_position = search_position.add_x(x).add_y(y);
        }

        let value = grid.get(&search_position);
        (search_position, value.clone())
    }

    fn next_cube(&self, grid: &Grid<char>) -> (Point, char) {
        let (x, y) = (self.direction.x(), self.direction.y());
        let bound = grid.bounds(0);
        let mut search_position = match (x, y) {
            (1, 0) => Point::new_2d(bound.lower().x(), self.position.y()),
            (-1, 0) => Point::new_2d(bound.upper().x(), self.position.y()),
            (0, 1) => Point::new_2d(self.position.x(), bound.lower().y()),
            (0, -1) => Point::new_2d(self.position.x(), bound.upper().y()),
            _ => unreachable!(),
        };
        
        while !grid.contains(&search_position) {
            search_position = search_position.add_x(x).add_y(y);
        }

        let value = grid.get(&search_position);
        (search_position, value.clone())
    }

    fn score(&self) -> i64 {
        let row_score = (self.position.y() + 1) * 1_000;
        let column_score = (self.position.x() + 1) * 4;
        let direction_score = match (self.direction.x(), self.direction.y()) {
            (1, 0) => 0,
            (0, 1) => 1,
            (-1, 0) => 2,
            (0, -1) => 3,
            _ => unreachable!(),
        };
        row_score + column_score + direction_score
    }
}
```

```
fn simulate(as_cube: bool) -> i64 {
    let (grid, instructions) = get_input();
    let mut state = get_start_state(&grid);
    for instruction in instructions {
        state.apply(&instruction, &grid, as_cube);
    }
    state.score()
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
```
