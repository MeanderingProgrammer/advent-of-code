use aoc_lib::answer;
use aoc_lib::point::Point;
use aoc_lib::reader;

fn main() {
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

    for rock_formation in rock_formations {
        println!("{:?}", rock_formation);
        for edge in rock_formation {
            println!("{:?}", edge);
        }
    }

    //answer::part1(v1, s1);
    //answer::part2(v2, s2);
}
