use aoc::prelude::*;

#[derive(Debug)]
struct UnionFind {
    parents: Vec<usize>,
    ranks: Vec<usize>,
}

impl UnionFind {
    fn new(n: usize) -> Self {
        Self {
            parents: (0..n).collect(),
            ranks: vec![1; n],
        }
    }

    fn union(&mut self, n1: usize, n2: usize) -> bool {
        let (p1, p2) = (self.find(n1), self.find(n2));
        if p1 == p2 {
            false
        } else {
            let (r1, r2) = (self.ranks[p1], self.ranks[p2]);
            let (parent, child) = if r1 >= r2 { (p1, p2) } else { (p2, p1) };
            self.parents[child] = parent;
            self.ranks[parent] += self.ranks[child];
            self.ranks[child] = 0;
            true
        }
    }

    fn find(&self, n: usize) -> usize {
        if self.parents[n] == n {
            n
        } else {
            self.find(self.parents[n])
        }
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let points = Reader::default().lines::<Point3d>();

    let mut circuit = UnionFind::new(points.len());

    let mut edges = points
        .iter()
        .enumerate()
        .flat_map(|(i1, p1)| {
            points
                .iter()
                .enumerate()
                .skip(i1 + 1)
                .map(move |(i2, p2)| (i1, i2, p1.euclidean(p2)))
        })
        .collect::<Vec<_>>();
    edges.sort_by(|(_, _, d1), (_, _, d2)| d1.total_cmp(d2));

    let mut components = points.len();
    let mut nth = None;
    let mut last = None;
    for (i, (n1, n2, _)) in edges.into_iter().enumerate() {
        if circuit.union(n1, n2) {
            components -= 1;
        }
        if i == 999 {
            nth = Some(circuit.ranks.clone());
        }
        if components == 1 {
            last = Some((n1, n2));
            break;
        }
    }

    let mut nth = nth.unwrap();
    nth.sort();
    let part1 = nth.iter().rev().take(3).product();

    let (n1, n2) = last.unwrap();
    let (x1, x2) = (points[n1].x, points[n2].x);
    let part2 = (x1 as usize) * (x2 as usize);

    answer::part1(181584, part1);
    answer::part2(8465902405, part2);
}
