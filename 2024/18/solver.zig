const std = @import("std");
const Allocator = std.mem.Allocator;
const aoc = @import("aoc");
const answer = aoc.answer;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;

const Search = struct {
    allocator: Allocator,
    points: std.ArrayList(Point),
    size: i64,

    fn solve(self: Search, n: usize) !?usize {
        var walls = Set(Point).init(self.allocator);
        defer walls.deinit();
        for (0..n) |i| {
            try walls.add(self.points.items[i]);
        }

        var seen = Set(Point).init(self.allocator);
        defer seen.deinit();

        var q = std.ArrayList(struct { Point, usize }).init(self.allocator);
        defer q.deinit();
        try q.append(.{ Point.init(0, 0), 0 });

        while (q.items.len > 0) {
            const node = q.orderedRemove(0);
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
                if (self.inside(neighbor) and !walls.contains(neighbor)) {
                    try q.append(.{ neighbor, steps + 1 });
                }
            }
        }
        return null;
    }

    fn inside(self: Search, p: Point) bool {
        return p.x >= 0 and p.y >= 0 and p.x <= self.size and p.y <= self.size;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const points = try Reader.init(allocator).lines(Point, parsePoint);
    const params = [2]usize{ 70, 1024 };
    const search = Search{ .allocator = allocator, .points = points, .size = params[0] };
    answer.part1(usize, 318, try part1(search, params[1]));
    answer.part2([]const u8, "56,29", try part2(allocator, search, params[1]));
}

fn parsePoint(_: Allocator, line: []const u8) !Point {
    var it = std.mem.splitScalar(u8, line, ',');
    const x = try aoc.util.decimal(i64, it.next().?);
    const y = try aoc.util.decimal(i64, it.next().?);
    return Point.init(x, y);
}

fn part1(search: Search, n: usize) !usize {
    return (try search.solve(n)).?;
}

fn part2(allocator: Allocator, search: Search, start: usize) ![]const u8 {
    var lo: usize = start;
    var hi: usize = search.points.items.len - 1;
    while (lo < hi) {
        const mid = (lo + hi) / 2;
        const solvable = try search.solve(mid) != null;
        if (solvable) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    const point = search.points.items[lo - 1];
    return try std.fmt.allocPrint(allocator, "{},{}", .{ point.x, point.y });
}
