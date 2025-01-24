use aoc_lib::answer;
use aoc_lib::grid::Grid;
use aoc_lib::reader::Reader;
use aoc_lib::search::Dijkstra;
use std::collections::BTreeMap;
use std::ops::Range;

// ...........
//   B C B D
//   D C B A
//   D B A C
//   A D C A
//
// Hall Width  = 2 + (4 + 3) + 2 = 11
// Pods / Room = 2 or 4

const WIDTH: u8 = 11;

#[derive(Debug)]
enum Hall {
    Open,
    Door,
}

impl From<u8> for Hall {
    fn from(value: u8) -> Self {
        match value {
            2 | 4 | 6 | 8 => Self::Door,
            _ => Self::Open,
        }
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
enum Pod {
    A,
    B,
    C,
    D,
}

impl Pod {
    fn from_char(ch: char) -> Option<Self> {
        match ch {
            'A' => Some(Self::A),
            'B' => Some(Self::B),
            'C' => Some(Self::C),
            'D' => Some(Self::D),
            _ => None,
        }
    }

    fn col(&self) -> u8 {
        match self {
            Self::A => 2,
            Self::B => 4,
            Self::C => 6,
            Self::D => 8,
        }
    }

    fn cost(&self) -> i64 {
        match self {
            Self::A => 1,
            Self::B => 10,
            Self::C => 100,
            Self::D => 1000,
        }
    }

    fn correct(&self, id: u8) -> bool {
        self.col() == Self::x(id)
    }

    fn path(&self, id: u8) -> Range<u8> {
        let (x1, x2) = (self.col(), Self::x(id));
        x1.min(x2) + 1..x1.max(x2)
    }

    fn id(x: u8, y: u8) -> u8 {
        (y * WIDTH) + x
    }

    fn x(id: u8) -> u8 {
        id % WIDTH
    }

    fn y(id: u8) -> u8 {
        id / WIDTH
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Burrow {
    pods: BTreeMap<u8, Pod>,
    size: u8,
}

impl Burrow {
    fn new(lines: &[String]) -> Self {
        let pods: BTreeMap<u8, Pod> = Grid::from_lines(lines, |_, ch| Pod::from_char(ch))
            .iter()
            .map(|(p, pod)| (Pod::id(p.x as u8, p.y as u8), pod.clone()))
            .collect();
        let size = (pods.len() / 4) as u8;
        Self { pods, size }
    }

    fn has(&self, id: u8) -> bool {
        self.pods.contains_key(&id)
    }

    fn done(&self) -> bool {
        self.pods.iter().all(|(id, pod)| pod.correct(*id))
    }

    fn neighbors(&self) -> impl Iterator<Item = (Self, i64)> + '_ {
        let mut room: Vec<(u8, u8)> = Vec::default();
        let mut hall: Vec<(u8, u8)> = Vec::default();
        self.pods
            .iter()
            .map(|(start, pod)| (*start, self.neighbor(*start, pod)))
            .for_each(|(start, mut ends)| {
                if ends.len() == 1 && Pod::y(ends[0]) == 0 {
                    room.push((start, ends.pop().unwrap()));
                } else {
                    ends.into_iter().for_each(|end| hall.push((start, end)));
                }
            });
        // If we can go to a room only make those moves
        let moves = if !room.is_empty() { room } else { hall };
        moves.into_iter().map(|(start, end)| self.apply(start, end))
    }

    fn neighbor(&self, start: u8, pod: &Pod) -> Vec<u8> {
        let (x, y) = (Pod::x(start), Pod::y(start));
        if y > 0 {
            // Pod: in a room
            let top = (1..y).map(|y| Pod::id(x, y)).all(|id| !self.has(id));
            if !top {
                // Pod: in a room & not at top
                //   -> can't move
                vec![]
            } else {
                // Pod: in a room & at the top
                if pod.correct(start) {
                    // Pod: in a room & at the top & correct
                    let below_settled = (y + 1..=self.size)
                        .map(|y| Pod::id(x, y))
                        .filter_map(|id| self.pods.get(&id).map(|pod| (id, pod)))
                        .all(|(id, pod)| pod.correct(id));
                    if below_settled {
                        // Pod: in a room & at the top & correct & below settled
                        //   -> in its final position
                        vec![]
                    } else {
                        // Pod: in a room & at the top & correct & below not settled
                        //   -> need to move somewhere in the hall
                        self.hall(start, pod)
                    }
                } else {
                    // Pod: in a room & at the top & not correct
                    //   -> try to move to correct room, fallback to hall
                    self.room(start, pod)
                        .map(|point| vec![point])
                        .unwrap_or_else(|| self.hall(start, pod))
                }
            }
        } else {
            // Pod: in the hall
            //   -> try to move pod to correct room
            self.room(start, pod)
                .map(|point| vec![point])
                .unwrap_or_default()
        }
    }

    fn room(&self, start: u8, pod: &Pod) -> Option<u8> {
        match self.in_room(pod.col()) {
            None => None,
            Some(room) => {
                let blocked = pod.path(start).any(|x| self.has(x));
                if blocked {
                    None
                } else {
                    Some(Pod::id(pod.col(), self.size - room))
                }
            }
        }
    }

    fn in_room(&self, x: u8) -> Option<u8> {
        let mut count = 0;
        for (id, pod) in self.pods.iter() {
            if Pod::x(*id) == x {
                if pod.col() != x {
                    return None;
                } else {
                    count += 1;
                }
            }
        }
        Some(count)
    }

    fn hall(&self, start: u8, pod: &Pod) -> Vec<u8> {
        let mut result = self.side(start, pod, true);
        result.append(&mut self.side(start, pod, false));
        result
    }

    fn side(&self, start: u8, pod: &Pod, left: bool) -> Vec<u8> {
        let x = Pod::x(start);
        let range: Box<dyn Iterator<Item = u8>> = if left {
            Box::new((0..x).rev())
        } else {
            Box::new(x + 1..WIDTH)
        };
        range
            .take_while(|end| !self.has(*end))
            .filter(|end| self.valid(pod, *end))
            .collect()
    }

    fn valid(&self, pod: &Pod, end: u8) -> bool {
        match end.into() {
            // Never stop outside of a room
            Hall::Door => false,
            Hall::Open => {
                // Detect "deadlock", occurs when we put a pod in the hall
                // and some pod is blocking it and we're blocking that pod
                pod.path(end).all(|id| {
                    self.pods
                        .get(&id)
                        .map(|pod| !pod.path(id).contains(&end))
                        .unwrap_or(true)
                })
            }
        }
    }

    fn apply(&self, start: u8, end: u8) -> (Self, i64) {
        let mut burrow = self.clone();
        let pod = burrow.pods.remove(&start).unwrap();
        let cost = pod.cost();
        // Movement along x-axis work as usual. Movement along the y-axis
        // needs to go up to hall then back down to our destination.
        // Example: hall is at y = 0, move y = 3 -> y = 1, means we go
        // from 3 -> 0 + 1 -> 0 = 3 + 1 = 4 (instead of 2).
        let (x1, x2) = (Pod::x(start) as i64, Pod::x(end) as i64);
        let (y1, y2) = (Pod::y(start) as i64, Pod::y(end) as i64);
        let distance = (x1 - x2).abs() + y1 + y2;
        burrow.pods.insert(end, pod);
        (burrow, cost * distance)
    }
}

#[derive(Debug)]
struct Search {}

impl Dijkstra for Search {
    type T = Burrow;

    fn done(&self, node: &Burrow) -> bool {
        node.done()
    }

    fn neighbors(&self, node: &Burrow) -> impl Iterator<Item = (Burrow, i64)> {
        node.neighbors()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    answer::part1(18282, solve(lines.clone(), false));
    answer::part2(50132, solve(lines.clone(), true));
}

fn solve(lines: Vec<String>, extend: bool) -> i64 {
    let lines = process_lines(lines, extend);
    let burrow = Burrow::new(&lines);
    Search {}.run(burrow).unwrap()
}

fn process_lines(lines: Vec<String>, extend: bool) -> Vec<String> {
    // #############
    // #...........#
    // ###B#C#B#D###
    //   #A#D#C#A#
    //   #########
    let mut result: Vec<String> = lines
        .into_iter()
        .skip(1)
        .take(3)
        .map(|s| s.replace('#', " "))
        .map(|s| s[1..s.len() - 1].to_string())
        .collect();
    // ...........
    //   B C B D
    //   A D C A
    if extend {
        result.insert(2, "  D C B A".to_string());
        result.insert(3, "  D B A C".to_string());
    }
    result
}
