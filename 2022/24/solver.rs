use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::reader;

type BlizzardGrid = Grid<char>;

struct Blizzard {
    grid: BlizzardGrid,
}

impl Blizzard {
    fn new(grid: BlizzardGrid) -> Self {
        Blizzard { grid }
    }

    fn next(&mut self) {

    }
}

fn main() {
    let mut blizzard = Blizzard::new(reader::read_grid(|ch| match ch {
        '<' | '^' | '>' | 'v' => Some(ch),
        _ => None,    
    }));
    println!("{}", blizzard.grid);
    println!("");
    blizzard.next();
    println!("{}", blizzard.grid);

    //answer::part1(v1, s1);
    //answer::part2(v2, s2);
}
