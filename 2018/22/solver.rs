use aoc::{Dijkstra, Direction, Grid, HashSet, Point, Reader, answer};

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
enum Tool {
    Gear,
    #[default]
    Torch,
    Neither,
}

#[derive(Debug)]
struct Region {
    erosion: usize,
    kind: usize,
    tools: HashSet<Tool>,
}

impl Region {
    fn new(erosion: usize) -> Self {
        let kind = erosion % 3;
        Self {
            erosion,
            kind,
            tools: match kind {
                0 => HashSet::from_iter([Tool::Gear, Tool::Torch]),
                1 => HashSet::from_iter([Tool::Gear, Tool::Neither]),
                2 => HashSet::from_iter([Tool::Torch, Tool::Neither]),
                _ => unreachable!(),
            },
        }
    }
}

#[derive(Debug)]
struct Cave {
    buffer: i32,
    depth: usize,
    target: Point,
    cave: Grid<Region>,
}

impl Cave {
    fn new(lines: &[String]) -> Self {
        let (_, depth) = lines[0].split_once(": ").unwrap();
        let (_, target) = lines[1].split_once(": ").unwrap();
        Self {
            buffer: 30,
            depth: depth.parse().unwrap(),
            target: target.parse().unwrap(),
            cave: Grid::default(),
        }
    }

    fn build(&mut self) {
        for x in 0..=self.target.x + self.buffer {
            for y in 0..=self.target.y + self.buffer {
                let point = Point::new(x, y);
                let region = self.region(&point);
                self.cave.add(point, region);
            }
        }
    }

    fn region(&self, point: &Point) -> Region {
        let index = if point == &Point::default() || point == &self.target {
            0
        } else if point.y == 0 {
            (point.x as usize) * 16_807
        } else if point.x == 0 {
            (point.y as usize) * 48_271
        } else {
            let left = &self.cave[&point.add(&Direction::Left)];
            let above = &self.cave[&point.add(&Direction::Up)];
            left.erosion * above.erosion
        };
        Region::new((index + self.depth) % 20_183)
    }

    fn risk(&self) -> usize {
        self.cave
            .iter()
            .filter(|(point, _)| point.x <= self.target.x && point.y <= self.target.y)
            .map(|(_, region)| region.kind)
            .sum()
    }
}

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
struct Node {
    point: Point,
    tool: Tool,
}

impl Node {
    fn new(point: Point, tool: Tool) -> Self {
        Self { point, tool }
    }
}

impl Dijkstra for Cave {
    type T = Node;
    type W = u16;

    fn done(&self, node: &Self::T) -> bool {
        node == &Node::new(self.target.clone(), Tool::default())
    }

    fn neighbors(&self, node: &Self::T) -> impl Iterator<Item = (Self::T, Self::W)> {
        let Node { point, tool } = node;
        let mut result = Vec::default();
        if point == &self.target {
            result.push((Node::new(point.clone(), Tool::default()), 7));
        } else {
            let tools = &self.cave[point].tools;
            for neighbor in point.neighbors() {
                if self.cave.has(&neighbor) {
                    let region = &self.cave[&neighbor];
                    if region.tools.contains(tool) {
                        result.push((Node::new(neighbor, tool.clone()), 1));
                    } else {
                        region
                            .tools
                            .intersection(tools)
                            .map(|tool| Node::new(neighbor.clone(), tool.clone()))
                            .for_each(|node| result.push((node, 8)));
                    }
                }
            }
        }
        result.into_iter()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().lines();
    let mut cave = Cave::new(&lines);
    cave.build();
    answer::part1(11575, cave.risk());
    answer::part2(1068, cave.run(Node::default()).unwrap());
}
