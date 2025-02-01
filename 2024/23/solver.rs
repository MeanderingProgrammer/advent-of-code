use aoc::{answer, HashMap, HashSet, Iter, Reader};

#[derive(Debug, Default)]
struct Graph {
    edges: HashMap<String, HashSet<String>>,
}

impl Graph {
    fn add(&mut self, line: String) {
        let (left, right) = line.split_once("-").unwrap();
        self.add_edge(left.to_string(), right.to_string());
        self.add_edge(right.to_string(), left.to_string());
    }

    fn add_edge(&mut self, from: String, to: String) {
        self.edges.entry(from).or_default().insert(to);
    }

    fn nodes(&self) -> HashSet<String> {
        self.edges.keys().cloned().collect()
    }

    // https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    fn bron_kerbosch(
        &self,
        r: Vec<String>,
        mut p: HashSet<String>,
        mut x: HashSet<String>,
    ) -> Vec<Vec<String>> {
        // if P and X are both empty then
        if p.is_empty() && x.is_empty() {
            // report R as a maximal clique
            return vec![r];
        }
        // choose a pivot vertex u in P ⋃ X
        let i = fastrand::usize(0..(p.len() + x.len()));
        let u = if i < p.len() {
            p.iter().nth(i).unwrap().clone()
        } else {
            x.iter().nth(i - p.len()).unwrap().clone()
        };
        // P \ N(u)
        let p_nu = p.clone();
        let nu = self.edges.get(&u).unwrap();
        // for each vertex v in P \ N(u) do
        p_nu.difference(nu)
            .flat_map(|v| {
                // R ⋃ {v}
                let mut r_v = r.clone();
                r_v.push(v.clone());
                r_v.sort();
                // BronKerbosch(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
                let nv = self.edges.get(v).unwrap();
                let partial = self.bron_kerbosch(
                    r_v,
                    p.intersection(nv).cloned().collect(),
                    x.intersection(nv).cloned().collect(),
                );
                // P := P \ {v}
                p.remove(v);
                // X := X ⋃ {v}
                x.insert(v.clone());
                partial
            })
            .collect()
    }
}

fn main() {
    answer::timer(solution);
}

fn solution() {
    let lines = Reader::default().read_lines();
    let cliques = get_cliques(lines);
    answer::part1(1215, part1(&cliques));
    answer::part2("bm,by,dv,ep,ia,ja,jb,ks,lv,ol,oy,uz,yt", &part2(&cliques));
}

fn get_cliques(lines: Vec<String>) -> Vec<Vec<String>> {
    let mut graph = Graph::default();
    lines.into_iter().for_each(|line| graph.add(line));
    graph.bron_kerbosch(Vec::default(), graph.nodes(), HashSet::default())
}

fn part1(cliques: &[Vec<String>]) -> usize {
    cliques
        .iter()
        .filter(|clique| clique.len() >= 3)
        .flat_map(|clique| clique.iter().combinations(3))
        .filter(|values| values.iter().any(|value| value.starts_with("t")))
        .unique()
}

fn part2(cliques: &[Vec<String>]) -> String {
    cliques
        .iter()
        .max_by_key(|clique| clique.len())
        .unwrap()
        .join(",")
}
