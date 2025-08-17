const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const Pair = struct { []const u8, []const u8 };
const Strings = std.ArrayList([]const u8);

const Logic = enum {
    AND,
    OR,
    XOR,

    fn init(line: []const u8) !Logic {
        if (std.mem.eql(u8, line, "AND")) {
            return Logic.AND;
        } else if (std.mem.eql(u8, line, "OR")) {
            return Logic.OR;
        } else if (std.mem.eql(u8, line, "XOR")) {
            return Logic.XOR;
        } else {
            return error.InvalidGate;
        }
    }
};

const Gate = struct {
    in1: []const u8,
    logic: Logic,
    in2: []const u8,

    fn init(line: []const u8) !Gate {
        // ntg XOR fgs
        var it = std.mem.splitScalar(u8, line, ' ');
        return .{
            .in1 = it.next().?,
            .logic = try Logic.init(it.next().?),
            .in2 = it.next().?,
        };
    }

    fn has(self: Gate, value: []const u8) bool {
        return std.mem.eql(u8, self.in1, value) or std.mem.eql(u8, self.in2, value);
    }

    fn eql(self: Gate, other: Gate) bool {
        return self.has(other.in1) and self.logic == other.logic and self.has(other.in2);
    }
};

const Graph = struct {
    allocator: std.mem.Allocator,
    output: std.StringHashMap(u8),
    gates: std.StringHashMap(Gate),

    fn init(allocator: std.mem.Allocator) Graph {
        return .{
            .allocator = allocator,
            .output = std.StringHashMap(u8).init(allocator),
            .gates = std.StringHashMap(Gate).init(allocator),
        };
    }

    fn clone(self: Graph) !Graph {
        return .{
            .allocator = self.allocator,
            .output = try self.output.clone(),
            .gates = try self.gates.clone(),
        };
    }

    fn addOutput(self: *Graph, line: []const u8) !void {
        // x00 = 1
        var it = std.mem.splitSequence(u8, line, ": ");
        const wire = it.next().?;
        const value = try aoc.util.decimal(u8, it.next().?);
        try self.output.put(wire, value);
    }

    fn addGate(self: *Graph, line: []const u8) !void {
        // ntg XOR fgs -> mjb
        var it = std.mem.splitSequence(u8, line, " -> ");
        const gate = try Gate.init(it.next().?);
        const out = it.next().?;
        try self.gates.put(out, gate);
    }

    fn simulate(self: *Graph) !usize {
        while (self.gates.count() > 0) {
            const outputs = try self.resolved();
            defer outputs.deinit();
            for (outputs.items) |output| {
                const gate = self.gates.get(output).?;
                const v1 = self.output.get(gate.in1).?;
                const v2 = self.output.get(gate.in2).?;
                const result = switch (gate.logic) {
                    Logic.AND => v1 & v2,
                    Logic.OR => v1 | v2,
                    Logic.XOR => v1 ^ v2,
                };
                try self.output.put(output, result);
                _ = self.gates.remove(output);
            }
        }
        return try self.get('z');
    }

    fn resolved(self: *Graph) !Strings {
        var result = Strings.init(self.allocator);
        var it = self.gates.iterator();
        while (it.next()) |entry| {
            const gate = entry.value_ptr;
            if (self.output.contains(gate.in1) and self.output.contains(gate.in2)) {
                try result.append(entry.key_ptr.*);
            }
        }
        return result;
    }

    fn get(self: Graph, ch: u8) !usize {
        const n = self.count(ch);
        var result = try self.allocator.alloc(u8, n);
        var output = self.output.iterator();
        while (output.next()) |entry| {
            const wire = entry.key_ptr.*;
            const value = entry.value_ptr.*;
            if (wire[0] == ch) {
                const i = try aoc.util.decimal(usize, wire[1..]);
                result[n - 1 - i] = '0' + value;
            }
        }
        return try std.fmt.parseInt(usize, result, 2);
    }

    fn count(self: Graph, ch: u8) usize {
        var result: usize = 0;
        var it = self.output.keyIterator();
        while (it.next()) |wire| {
            if (wire.*[0] == ch) {
                result += 1;
            }
        }
        return result;
    }

    // Unsure if this solution is general but good enough for my input
    fn fix(self: *Graph, i: u8) !?Pair {
        const z = try self.node('z', i);
        const root = self.gates.get(z).?;
        const xor = self.find(.{
            .in1 = try self.node('x', i),
            .logic = Logic.XOR,
            .in2 = try self.node('y', i),
        }).?;
        if (root.logic != Logic.XOR) {
            const replace = self.like(xor, Logic.XOR).?;
            return .{ z, replace };
        } else if (!root.has(xor)) {
            const in1_gate = self.gates.get(root.in1).?;
            const replace = if (in1_gate.logic != Logic.OR) root.in1 else root.in2;
            return .{ xor, replace };
        }
        return null;
    }

    fn find(self: *Graph, gate: Gate) ?[]const u8 {
        var it = self.gates.iterator();
        while (it.next()) |entry| {
            if (entry.value_ptr.eql(gate)) {
                return entry.key_ptr.*;
            }
        }
        return null;
    }

    fn like(self: *Graph, value: []const u8, logic: Logic) ?[]const u8 {
        var it = self.gates.iterator();
        while (it.next()) |entry| {
            if (entry.value_ptr.has(value) and entry.value_ptr.logic == logic) {
                return entry.key_ptr.*;
            }
        }
        return null;
    }

    fn node(self: *Graph, ch: u8, i: u8) ![]const u8 {
        var result = try self.allocator.alloc(u8, 3);
        result[0] = ch;
        result[1] = '0' + (i / 10);
        result[2] = '0' + (i % 10);
        return result;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const groups = try aoc.Reader.init(c.allocator()).groups();
    const graph = try getGraph(c.allocator(), groups);
    answer.part1(usize, 56939028423824, try part1(graph));
    answer.part2([]const u8, "frn,gmq,vtj,wnf,wtt,z05,z21,z39", try part2(c.allocator(), graph));
}

fn getGraph(allocator: std.mem.Allocator, groups: std.ArrayList(Strings)) !Graph {
    var graph = Graph.init(allocator);
    for (groups.items[0].items) |line| {
        try graph.addOutput(line);
    }
    for (groups.items[1].items) |line| {
        try graph.addGate(line);
    }
    return graph;
}

fn part1(input: Graph) !usize {
    var graph = try input.clone();
    return try graph.simulate();
}

fn part2(allocator: std.mem.Allocator, input: Graph) ![]const u8 {
    var graph = try input.clone();
    var result = Strings.init(allocator);
    for (1..graph.count('x')) |i| {
        if (try graph.fix(@intCast(i))) |wires| {
            try result.append(wires[0]);
            try result.append(wires[1]);
        }
    }
    std.mem.sort([]const u8, result.items, {}, stringLessThan);
    return std.mem.join(allocator, ",", result.items);
}

fn stringLessThan(_: void, lhs: []const u8, rhs: []const u8) bool {
    return std.mem.order(u8, lhs, rhs) == .lt;
}
