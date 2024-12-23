const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Strings = Set([]const u8);
const Graph = struct {
    nodes: Strings,
    edges: std.StringHashMap(Strings),

    fn init() Graph {
        return .{
            .nodes = Strings.init(allocator),
            .edges = std.StringHashMap(Strings).init(allocator),
        };
    }

    fn add(self: *Graph, line: []const u8) !void {
        var it = std.mem.splitScalar(u8, line, '-');
        const left = it.next().?;
        const right = it.next().?;
        try self.add_edge(left, right);
        try self.add_edge(right, left);
    }

    fn add_edge(self: *Graph, from: []const u8, to: []const u8) !void {
        try self.nodes.add(from);
        var entry = try self.edges.getOrPut(from);
        if (!entry.found_existing) {
            entry.value_ptr.* = Strings.init(allocator);
        }
        try entry.value_ptr.add(to);
    }

    fn bron_kerbosch(self: Graph, r: Strings, p: *Strings, x: *Strings, result: *std.ArrayList(Strings)) !void {
        if (p.size() == 0 and x.size() == 0) {
            try result.append(r);
            return;
        }

        // Choose an arbitrary node as the pivot
        var joined = try p.clone();
        try joined.extend(x.*);
        const pivot = joined.next();

        // Only consider nodes not connected to the pivot
        var difference = try p.clone();
        difference.difference(self.edges.get(pivot).?);

        var it = difference.iterator();
        while (it.next()) |node| {
            const v = node.*;
            var rc = try r.clone();
            try rc.add(v);
            var pc = try p.intersection(self.edges.get(v).?);
            var xc = try x.intersection(self.edges.get(v).?);
            try self.bron_kerbosch(rc, &pc, &xc, result);
            p.remove(v);
            try x.add(v);
        }
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const lines = try Reader.init().string_lines();
    const cliques = try get_cliques(lines);
    answer.part1(usize, 1215, try part1(cliques));
    answer.part2([]const u8, "bm,by,dv,ep,ia,ja,jb,ks,lv,ol,oy,uz,yt", try part2(cliques));
}

fn get_cliques(lines: std.ArrayList([]const u8)) !std.ArrayList(Strings) {
    var graph = Graph.init();
    for (lines.items) |line| {
        try graph.add(line);
    }
    const r = Strings.init(allocator);
    var p = try graph.nodes.clone();
    var x = Strings.init(allocator);
    var result = std.ArrayList(Strings).init(allocator);
    try graph.bron_kerbosch(r, &p, &x, &result);
    return result;
}

fn part1(cliques: std.ArrayList(Strings)) !usize {
    var result = Strings.init(allocator);
    for (cliques.items) |clique| {
        if (clique.size() >= 3) {
            try combinations(&result, try clique.list());
        }
    }
    return result.size();
}

fn combinations(result: *Strings, clique: std.ArrayList([]const u8)) !void {
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
                    try result.add(try str(option));
                }
            }
        }
    }
}

fn part2(cliques: std.ArrayList(Strings)) ![]const u8 {
    var index: usize = 0;
    for (1..cliques.items.len) |i| {
        if (cliques.items[i].size() > cliques.items[index].size()) {
            index = i;
        }
    }
    return try str(cliques.items[index]);
}

fn str(nodes: Strings) ![]const u8 {
    const result = try nodes.list();
    std.mem.sort([]const u8, result.items, {}, string_less_than);
    return std.mem.join(allocator, ",", result.items);
}

fn string_less_than(_: void, lhs: []const u8, rhs: []const u8) bool {
    return std.mem.order(u8, lhs, rhs) == .lt;
}
