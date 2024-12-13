const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Points = std.ArrayList(Point);
const Groups = std.AutoHashMap(u8, Group);
const Group = struct {
    grid: Grid,
    points: Points,

    fn init(grid: Grid) Group {
        return Group{ .grid = grid, .points = Points.init(allocator) };
    }

    fn append(self: *Group, point: Point) !void {
        try self.points.append(point);
    }

    fn antinodes(self: *Group, resonate: bool) !Points {
        var result = Points.init(allocator);
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

    fn walk(self: *Group, points: *Points, start: Point, slope: Point) !void {
        var point = start;
        while (try self.add(points, point)) {
            point = point.plus(slope);
        }
    }

    fn add(self: *Group, points: *Points, point: Point) !bool {
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

fn solution() !void {
    const grid = try Reader.init().grid();
    const groups = try group(grid);
    answer.part1(usize, 320, try num_antinodes(groups, false));
    answer.part2(usize, 1157, try num_antinodes(groups, true));
}

fn group(grid: Grid) !Groups {
    var result = Groups.init(allocator);
    var points = grid.points();
    while (points.next()) |point| {
        const value = grid.get(point.*).?;
        if (value != '.') {
            const entry = try result.getOrPut(value);
            if (!entry.found_existing) {
                entry.value_ptr.* = Group.init(grid);
            }
            try entry.value_ptr.append(point.*);
        }
    }
    return result;
}

fn num_antinodes(groups: Groups, resonate: bool) !usize {
    var result = Set(Point).init(allocator);
    var it = groups.iterator();
    while (it.next()) |entry| {
        const antinodes = try entry.value_ptr.antinodes(resonate);
        for (antinodes.items) |point| {
            try result.add(point);
        }
    }
    return result.size();
}
