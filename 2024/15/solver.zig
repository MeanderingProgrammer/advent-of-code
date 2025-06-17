const aoc = @import("aoc");
const answer = aoc.answer;
const Direction = aoc.point.Direction;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Warehouse = struct {
    grid: Grid,
    position: Point,

    fn init(lines: std.ArrayList([]const u8), wide: bool) !Warehouse {
        var grid = try Grid.init(if (wide) try enlarge(lines) else lines);
        const start = (try grid.getValues('@')).getLast();
        try grid.set(start, '.');
        return .{
            .grid = grid,
            .position = start,
        };
    }

    fn enlarge(lines: std.ArrayList([]const u8)) !std.ArrayList([]const u8) {
        var result = std.ArrayList([]const u8).init(allocator);
        for (lines.items) |line| {
            var l = std.ArrayList(u8).init(allocator);
            for (line) |ch| {
                if (ch == 'O') {
                    try l.append('[');
                    try l.append(']');
                } else if (ch == '@') {
                    try l.append('@');
                    try l.append('.');
                } else {
                    try l.appendNTimes(ch, 2);
                }
            }
            try result.append(l.items);
        }
        return result;
    }

    fn go(self: *Warehouse, direction: Direction) !void {
        if (try self.move(direction)) |points| {
            self.position = self.position.plus(direction.point());
            var unset_it = points.iterator();
            while (unset_it.next()) |entry| {
                const point = entry.key_ptr.*;
                try self.grid.set(point, '.');
            }
            var set_it = points.iterator();
            while (set_it.next()) |entry| {
                const point = entry.key_ptr.*;
                const value = entry.value_ptr.*;
                try self.grid.set(point.plus(direction.point()), value);
            }
        }
    }

    fn move(self: *Warehouse, direction: Direction) !?std.AutoHashMap(Point, u8) {
        var result = std.AutoHashMap(Point, u8).init(allocator);
        try result.put(self.position, '.');
        while (true) {
            var additional = Set(Point).init(allocator);
            var exiting_it = result.keyIterator();
            while (exiting_it.next()) |p| {
                const point = p.*.plus(direction.point());
                if (!result.contains(point)) {
                    const value = self.grid.get(point).?;
                    if (value == '#') {
                        return null;
                    } else if (value == 'O') {
                        try additional.add(point);
                    } else if (value == '[') {
                        try additional.add(point);
                        try additional.add(point.plus(Direction.e.point()));
                    } else if (value == ']') {
                        try additional.add(point);
                        try additional.add(point.plus(Direction.w.point()));
                    }
                }
            }
            if (additional.size() == 0) {
                return result;
            } else {
                var additional_it = additional.iterator();
                while (additional_it.next()) |p| {
                    const point = p.*;
                    try result.put(point, self.grid.get(point).?);
                }
            }
        }
        return null;
    }

    fn gps(self: Warehouse) i64 {
        var result: i64 = 0;
        var points = self.grid.points();
        while (points.next()) |point| {
            const value = self.grid.get(point.*).?;
            if (value == 'O' or value == '[') {
                result += ((100 * point.y) + point.x);
            }
        }
        return result;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const groups = try Reader.init().groups();
    const lines = groups.items[0];
    const directions = try getDirections(groups.items[1]);
    answer.part1(i64, 1442192, try solve(lines, false, directions));
    answer.part2(i64, 1448458, try solve(lines, true, directions));
}

fn getDirections(lines: std.ArrayList([]const u8)) !std.ArrayList(Direction) {
    var directions = std.ArrayList(Direction).init(allocator);
    for (lines.items) |line| {
        for (line) |ch| {
            try directions.append(Direction.init(ch).?);
        }
    }
    return directions;
}

fn solve(lines: std.ArrayList([]const u8), wide: bool, directions: std.ArrayList(Direction)) !i64 {
    var warehouse = try Warehouse.init(lines, wide);
    for (directions.items) |direction| {
        try warehouse.go(direction);
    }
    return warehouse.gps();
}
