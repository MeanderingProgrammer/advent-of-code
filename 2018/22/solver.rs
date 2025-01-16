use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::point::{Direction, Point};
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;
use std::collections::HashSet;

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
                0 => [Tool::Gear, Tool::Torch].into(),
                1 => [Tool::Gear, Tool::Neither].into(),
                2 => [Tool::Torch, Tool::Neither].into(),
                _ => unreachable!(),
            },
        }
    }
}

#[derive(Debug)]
struct Cave {
    buffer: i64,
    depth: usize,
    target: Point,
    cave: Grid<Region>,
}

impl Cave {
    fn new(lines: &[String]) -> Self {
        Self {
            buffer: 30,
            depth: Self::second(&lines[0]).parse().unwrap(),
            target: Self::second(&lines[1]).parse().unwrap(),
            cave: Grid::default(),
        }
    }

    fn second(s: &str) -> &str {
        s.split_once(": ").unwrap().1
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
            let left = self.cave.get(&(point + &Direction::Left));
            let above = self.cave.get(&(point + &Direction::Up));
            left.erosion * above.erosion
        };
        Region::new((index + self.depth) % 20_183)
    }

    fn risk(&self) -> usize {
        self.cave
            .points()
            .into_iter()
            .filter(|point| point.x <= self.target.x && point.y <= self.target.y)
            .map(|point| self.cave.get(point))
            .map(|region| region.kind)
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

    fn done(&self, node: &Node) -> bool {
        node == &Node::new(self.target.clone(), Tool::default())
    }

    fn neighbors(&self, node: &Node) -> impl Iterator<Item = (Node, i64)> {
        let Node { point, tool } = node;
        let mut result = Vec::default();
        if point == &self.target {
            result.push((Node::new(point.clone(), Tool::default()), 7));
        } else {
            let tools = &self.cave.get(point).tools;
            for neighbor in point.neighbors() {
                if self.cave.contains(&neighbor) {
                    let region = self.cave.get(&neighbor);
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
    let lines = Reader::default().read_lines();
    let mut cave = Cave::new(&lines);
    cave.build();
    answer::part1(11575, cave.risk());
    answer::part2(1068, cave.run(Node::default()).unwrap());
}
