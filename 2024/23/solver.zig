const std = @import("std");
const random = std.crypto.random;
const aoc = @import("aoc");
const answer = aoc.answer;

const Strings = aoc.Set([]const u8);

const Graph = struct {
    allocator: std.mem.Allocator,
    nodes: Strings,
    edges: std.StringHashMap(Strings),
    cliques: std.ArrayList(Strings),

    fn init(allocator: std.mem.Allocator) Graph {
        return .{
            .allocator = allocator,
            .nodes = Strings.init(allocator),
            .edges = std.StringHashMap(Strings).init(allocator),
            .cliques = std.ArrayList(Strings).init(allocator),
        };
    }

    fn add(self: *Graph, line: []const u8) !void {
        var it = std.mem.splitScalar(u8, line, '-');
        const left = it.next().?;
        const right = it.next().?;
        try self.addEdge(left, right);
        try self.addEdge(right, left);
    }

    fn addEdge(self: *Graph, from: []const u8, to: []const u8) !void {
        try self.nodes.add(from);
        var entry = try self.edges.getOrPut(from);
        if (!entry.found_existing) {
            entry.value_ptr.* = Strings.init(self.allocator);
        }
        try entry.value_ptr.add(to);
    }

    // https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    fn bronKerbosch(self: *Graph, r: Strings, p: *Strings, x: *Strings) !void {
        // if P and X are both empty then
        if (p.size() == 0 and x.size() == 0) {
            // report R as a maximal clique
            try self.cliques.append(r);
            return;
        }
        // choose a pivot vertex u in P ⋃ X
        const i = random.uintLessThan(usize, p.size() + x.size());
        const u = if (i < p.size()) p.nth(i) else x.nth(i - p.size());
        // P \ N(u)
        var p_nu = try p.clone();
        p_nu.difference(self.edges.get(u).?);
        // for each vertex v in P \ N(u) do
        var it = p_nu.iterator();
        while (it.next()) |vertex| {
            const v = vertex.*;
            // R ⋃ {v}
            var r_v = try r.clone();
            try r_v.add(v);
            // P ⋂ N(v)
            var p_nv = try p.intersection(self.edges.get(v).?);
            // X ⋂ N(v)
            var x_nv = try x.intersection(self.edges.get(v).?);
            // BronKerbosch(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
            try self.bronKerbosch(r_v, &p_nv, &x_nv);
            // P := P \ {v}
            p.remove(v);
            // X := X ⋃ {v}
            try x.add(v);
        }
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const lines = try aoc.Reader.init(c.allocator()).stringLines();
    const cliques = try getCliques(c.allocator(), lines);
    answer.part1(usize, 1215, try part1(c.allocator(), cliques));
    answer.part2([]const u8, "bm,by,dv,ep,ia,ja,jb,ks,lv,ol,oy,uz,yt", try part2(c.allocator(), cliques));
}

fn getCliques(allocator: std.mem.Allocator, lines: std.ArrayList([]const u8)) !std.ArrayList(Strings) {
    var graph = Graph.init(allocator);
    for (lines.items) |line| {
        try graph.add(line);
    }
    const r = Strings.init(allocator);
    var p = try graph.nodes.clone();
    var x = Strings.init(allocator);
    try graph.bronKerbosch(r, &p, &x);
    return graph.cliques;
}

fn part1(allocator: std.mem.Allocator, cliques: std.ArrayList(Strings)) !usize {
    var result = Strings.init(allocator);
    for (cliques.items) |clique| {
        if (clique.size() >= 3 and hasChief(clique)) {
            try combinations(allocator, &result, try clique.list());
        }
    }
    return result.size();
}

fn hasChief(clique: Strings) bool {
    var it = clique.iterator();
    while (it.next()) |v| {
        if (v.*[0] == 't') {
            return true;
        }
    }
    return false;
}

fn combinations(allocator: std.mem.Allocator, result: *Strings, clique: std.ArrayList([]const u8)) !void {
    for (0..clique.items.len - 2) |i| {
        for (i + 1..clique.items.len - 1) |j| {
            for (j + 1..clique.items.len) |k| {
                const iv = clique.items[i];
                const jv = clique.items[j];
                const kv = clique.items[k];
                if (iv[0] == 't' or jv[0] == 't' or kv[0] == 't') {
                    var option = Strings.init(allocator);
                    try option.add(iv);
                    try option.add(jv);
                    try option.add(kv);
                    try result.add(try str(allocator, option));
                }
            }
        }
    }
}

fn part2(allocator: std.mem.Allocator, cliques: std.ArrayList(Strings)) ![]const u8 {
    var index: usize = 0;
    for (1..cliques.items.len) |i| {
        if (cliques.items[i].size() > cliques.items[index].size()) {
            index = i;
        }
    }
    return try str(allocator, cliques.items[index]);
}

fn str(allocator: std.mem.Allocator, nodes: Strings) ![]const u8 {
    const result = try nodes.list();
    std.mem.sort([]const u8, result.items, {}, stringLessThan);
    return std.mem.join(allocator, ",", result.items);
}

fn stringLessThan(_: void, lhs: []const u8, rhs: []const u8) bool {
    return std.mem.order(u8, lhs, rhs) == .lt;
}
