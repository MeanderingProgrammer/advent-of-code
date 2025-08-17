const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const Points = std.ArrayList(aoc.Point);
const Groups = std.AutoHashMap(u8, Group);

const Group = struct {
    allocator: std.mem.Allocator,
    grid: aoc.Grid(u8),
    points: Points,

    fn init(allocator: std.mem.Allocator, grid: aoc.Grid(u8)) Group {
        return .{
            .allocator = allocator,
            .grid = grid,
            .points = Points.init(allocator),
        };
    }

    fn append(self: *Group, point: aoc.Point) !void {
        try self.points.append(point);
    }

    fn antinodes(self: *Group, resonate: bool) !Points {
        var result = Points.init(self.allocator);
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

    fn walk(self: *Group, points: *Points, start: aoc.Point, slope: aoc.Point) !void {
        var point = start;
        while (try self.add(points, point)) {
            point = point.plus(slope);
        }
    }

    fn add(self: *Group, points: *Points, point: aoc.Point) !bool {
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

fn group(allocator: std.mem.Allocator, grid: aoc.Grid(u8)) !Groups {
    var result = Groups.init(allocator);
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

fn numAntinodes(allocator: std.mem.Allocator, groups: Groups, resonate: bool) !usize {
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
