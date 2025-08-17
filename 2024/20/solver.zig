const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const State = struct {
    allocator: std.mem.Allocator,
    point: aoc.Point,
    path: std.ArrayList(aoc.Point),

    fn init(allocator: std.mem.Allocator, point: aoc.Point) !State {
        var path = std.ArrayList(aoc.Point).init(allocator);
        try path.append(point);
        return .{
            .allocator = allocator,
            .point = point,
            .path = path,
        };
    }

    fn neighbors(self: State) !std.ArrayList(State) {
        var result = std.ArrayList(State).init(self.allocator);
        for (self.point.neighbors()) |point| {
            var path = try self.path.clone();
            try path.append(point);
            try result.append(State{
                .allocator = self.allocator,
                .point = point,
                .path = path,
            });
        }
        return result;
    }
};

const Race = struct {
    allocator: std.mem.Allocator,
    grid: aoc.Grid(u8),
    start: aoc.Point,
    end: aoc.Point,
    paths: std.AutoHashMap(aoc.Point, std.ArrayList(aoc.Point)),

    fn init(allocator: std.mem.Allocator, grid: *aoc.Grid(u8)) !Race {
        const start = (try grid.getValues('S')).getLast();
        const end = (try grid.getValues('E')).getLast();
        try grid.put(start, '.');
        try grid.put(end, '.');
        return .{
            .allocator = allocator,
            .grid = grid.*,
            .start = start,
            .end = end,
            .paths = std.AutoHashMap(aoc.Point, std.ArrayList(aoc.Point)).init(allocator),
        };
    }

    fn solve(self: *Race) !void {
        var q = std.ArrayList(State).init(self.allocator);
        try q.append(try State.init(self.allocator, self.end));
        while (q.items.len > 0) {
            var current = q.orderedRemove(0);
            if (self.paths.contains(current.point)) {
                continue;
            }
            try self.paths.put(current.point, current.path);
            const neighbors = try current.neighbors();
            for (neighbors.items) |next| {
                if (self.grid.get(next.point).? != '.') {
                    continue;
                }
                try q.append(next);
            }
        }
    }

    fn cheats(self: Race, savings: usize, duration: usize) !usize {
        var result: usize = 0;
        const path = self.paths.get(self.start).?;
        const base_time = path.items.len;
        for (0..path.items.len) |i| {
            const point = path.items[path.items.len - 1 - i];
            for (rangeStart(point.x, duration)..rangeEnd(point.x, duration)) |x| {
                for (rangeStart(point.y, duration)..rangeEnd(point.y, duration)) |y| {
                    const option = aoc.Point.init(@intCast(x), @intCast(y));
                    const distance = point.manhattan(option);
                    if (distance < 2 or distance > duration) {
                        continue;
                    }
                    if (self.grid.get(option) orelse '#' != '.') {
                        continue;
                    }
                    const cheat_path = self.paths.get(option).?;
                    const cheat_time = i + distance + cheat_path.items.len;
                    if (cheat_time >= base_time) {
                        continue;
                    }
                    const saved = base_time - cheat_time;
                    if (saved >= savings) {
                        result += 1;
                    }
                }
            }
        }
        return result;
    }

    fn rangeStart(value: i64, offset: usize) usize {
        const v: usize = @intCast(value);
        return if (offset >= v) 0 else v - offset;
    }

    fn rangeEnd(value: i64, offset: usize) usize {
        const v: usize = @intCast(value);
        return v + offset + 1;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    var grid = try aoc.Reader.init(c.allocator()).grid();
    var race = try Race.init(c.allocator(), &grid);
    try race.solve();
    answer.part1(usize, 1399, try race.cheats(100, 2));
    answer.part2(usize, 994807, try race.cheats(100, 20));
}
