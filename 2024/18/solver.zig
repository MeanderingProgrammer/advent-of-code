const aoc = @import("aoc");
const answer = aoc.answer;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Grid = struct {
    size: i64,
    points: Set(Point),

    fn init(size: i64) Grid {
        return .{ .size = size, .points = Set(Point).init(allocator) };
    }

    fn add(self: *Grid, point: Point) !void {
        try self.points.add(point);
    }

    fn solve(self: Grid, order: bool) !?usize {
        var seen = Set(Point).init(allocator);
        defer seen.deinit();
        var q = std.ArrayList(struct { Point, usize }).init(allocator);
        defer q.deinit();
        try q.append(.{ Point.init(0, 0), 0 });
        while (q.items.len > 0) {
            const node = if (order) q.orderedRemove(0) else q.pop();
            const point: Point = node[0];
            const steps: usize = node[1];
            if (seen.contains(point)) {
                continue;
            }
            try seen.add(point);
            if (point.x == self.size and point.y == self.size) {
                return steps;
            }
            for (point.neighbors()) |neighbor| {
                if (neighbor.x < 0 or neighbor.y < 0) {
                    continue;
                }
                if (neighbor.x > self.size or neighbor.y > self.size) {
                    continue;
                }
                if (self.points.contains(neighbor)) {
                    continue;
                }
                try q.append(.{ neighbor, steps + 1 });
            }
        }
        return null;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const points = try Reader.init().lines(Point, parse_point);
    const params = [2]usize{ 70, 1024 };
    var grid = Grid.init(params[0]);
    answer.part1(usize, 318, try part1(&grid, points, params[1]));
    answer.part2([]const u8, "56,29", try part2(&grid, points, params[1]));
}

fn parse_point(line: []const u8) !Point {
    var it = std.mem.splitScalar(u8, line, ',');
    const x = try std.fmt.parseInt(i64, it.next().?, 10);
    const y = try std.fmt.parseInt(i64, it.next().?, 10);
    return Point.init(x, y);
}

fn part1(grid: *Grid, points: std.ArrayList(Point), n: usize) !usize {
    for (0..n) |i| {
        try grid.add(points.items[i]);
    }
    return (try grid.solve(true)).?;
}

fn part2(grid: *Grid, points: std.ArrayList(Point), start: usize) ![]const u8 {
    var i: usize = start;
    while (try grid.solve(false) != null) : (i += 1) {
        try grid.add(points.items[i]);
    }
    const point = points.items[i - 1];
    return try std.fmt.allocPrint(allocator, "{},{}", .{ point.x, point.y });
}
