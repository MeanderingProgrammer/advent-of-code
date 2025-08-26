const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.array_list.Managed;
const Map = std.AutoHashMap;

const aoc = @import("aoc");
const answer = aoc.answer;

const Group = struct {
    allocator: Allocator,
    grid: aoc.Grid(u8),
    points: List(aoc.Point),

    fn init(allocator: Allocator, grid: aoc.Grid(u8)) Group {
        return .{
            .allocator = allocator,
            .grid = grid,
            .points = List(aoc.Point).init(allocator),
        };
    }

    fn append(self: *Group, point: aoc.Point) !void {
        try self.points.append(point);
    }

    fn antinodes(self: *Group, resonate: bool) !List(aoc.Point) {
        var result = List(aoc.Point).init(self.allocator);
        const points = self.points.items;
        for (points, 0..) |p1, i| {
            for ((i + 1)..points.len) |j| {
                const p2 = points[j];
                const left = if (p1.x < p2.x) p1 else p2;
                const right = if (p1.x < p2.x) p2 else p1;
                const slope = left.minus(right);
                if (resonate) {
                    try self.walk(&result, left, slope);
                    try self.walk(&result, right, slope.negate());
                } else {
                    _ = try self.add(&result, left.plus(slope));
                    _ = try self.add(&result, right.plus(slope.negate()));
                }
            }
        }
        return result;
    }

    fn walk(self: *Group, points: *List(aoc.Point), start: aoc.Point, slope: aoc.Point) !void {
        var point = start;
        while (try self.add(points, point)) {
            point = point.plus(slope);
        }
    }

    fn add(self: *Group, points: *List(aoc.Point), point: aoc.Point) !bool {
        if (self.grid.get(point) == null) {
            return false;
        } else {
            try points.append(point);
            return true;
        }
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const grid = try aoc.Reader.init(c.allocator()).grid();
    const groups = try group(c.allocator(), grid);
    answer.part1(usize, 320, try numAntinodes(c.allocator(), groups, false));
    answer.part2(usize, 1157, try numAntinodes(c.allocator(), groups, true));
}

fn group(allocator: Allocator, grid: aoc.Grid(u8)) !Map(u8, Group) {
    var result = Map(u8, Group).init(allocator);
    var points = grid.points();
    while (points.next()) |point| {
        const value = grid.get(point.*).?;
        if (value != '.') {
            const entry = try result.getOrPut(value);
            if (!entry.found_existing) {
                entry.value_ptr.* = Group.init(allocator, grid);
            }
            try entry.value_ptr.append(point.*);
        }
    }
    return result;
}

fn numAntinodes(allocator: Allocator, groups: Map(u8, Group), resonate: bool) !usize {
    var result = aoc.Set(aoc.Point).init(allocator);
    var it = groups.iterator();
    while (it.next()) |entry| {
        const antinodes = try entry.value_ptr.antinodes(resonate);
        for (antinodes.items) |point| {
            try result.add(point);
        }
    }
    return result.size();
}
