use aoc::prelude::*;

#[derive(Debug, PartialEq)]
enum Value {
    On,
    Off,
}

impl FromChar for Value {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            '#' => Some(Self::On),
            _ => Some(Self::Off),
        }
    }
}

#[derive(Debug, Clone)]
struct Image {
    on: HashSet<Point>,
    enhancer: Vec<bool>,
    time: usize,
    border: Point,
}

impl Image {
    fn new(groups: &[String]) -> Self {
        let enhancer = groups[0].chars().map(|ch| ch == '#').collect();
        let grid: Grid<Value> = groups[1].as_str().into();
        Self {
            on: grid.values(&Value::On).into_iter().collect(),
            enhancer,
            time: 0,
            border: Point::new(1, 1),
        }
    }

    fn enhance(&mut self) {
        let mut on = HashSet::default();
        let bounds = Bounds::new(&self.on.iter().collect::<Vec<_>>());
        let start = bounds.lower.sub(self.border.clone());
        let end = bounds.upper.add(self.border.clone());
        for y in start.y..=end.y {
            for x in start.x..=end.x {
                let point = Point::new(x, y);
                if self.next(&bounds, &point) {
                    on.insert(point);
                }
            }
        }
        self.on = on;
        self.time += 1;
    }

    fn next(&self, bounds: &Bounds, point: &Point) -> bool {
        let mut binary = String::default();
        for dy in -1..=1 {
            for dx in -1..=1 {
                let neighbor = point.add(Point::new(dx, dy));
                let on = if bounds.contain(&neighbor) {
                    self.on.contains(&neighbor)
                } else {
                    self.edge()
                };
                binary.push(if on { '1' } else { '0' });
            }
        }
        let index = usize::from_str_radix(&binary, 2).unwrap();
        self.enhancer[index]
    }

    fn edge(&self) -> bool {
        let first = *self.enhancer.first().unwrap();
        let last = *self.enhancer.last().unwrap();
        let odd = self.time % 2 == 1;
        first && (last || odd)
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let groups = Reader::default().groups::<String>();
    let image = Image::new(&groups);
    answer::part1(5437, after(&image, 2));
    answer::part2(19340, after(&image, 50));
}

fn after(image: &Image, n: usize) -> usize {
    let mut image = image.clone();
    for _ in 0..n {
        image.enhance();
    }
    image.on.len()
}
