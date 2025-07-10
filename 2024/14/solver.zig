const aoc = @import("aoc");
const answer = aoc.answer;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
const std = @import("std");
const Allocator = std.mem.Allocator;

const Robot = struct {
    position: Point,
    velocity: Point,

    fn init(line: []const u8) !Robot {
        // p=0,4 v=3,-3
        var parts = std.mem.splitScalar(u8, line, ' ');
        return .{
            .position = try parsePoint(parts.next().?),
            .velocity = try parsePoint(parts.next().?),
        };
    }

    fn parsePoint(s: []const u8) !Point {
        var n_p = std.mem.splitBackwardsScalar(u8, s, '=');
        var x_y = std.mem.splitScalar(u8, n_p.next().?, ',');
        const x = try std.fmt.parseInt(i64, x_y.next().?, 10);
        const y = try std.fmt.parseInt(i64, x_y.next().?, 10);
        return Point.init(x, y);
    }

    fn move(self: *Robot, x: i64, y: i64) void {
        self.position = self.position.plus(self.velocity);
        self.position.x = @mod(self.position.x, x);
        self.position.y = @mod(self.position.y, y);
    }

    fn quadrant(self: Robot, x: i64, y: i64) ?usize {
        const px = self.position.x;
        const py = self.position.y;
        const mx = @divFloor(x, 2);
        const my = @divFloor(y, 2);
        if (px == mx or py == my) {
            return null;
        } else {
            const left = px < mx;
            const top = py < my;
            if (top and left) {
                return 0;
            } else if (top) {
                return 1;
            } else if (left) {
                return 2;
            } else {
                return 3;
            }
        }
    }
};

const Grid = struct {
    allocator: Allocator,
    x: i64,
    y: i64,
    robots: std.ArrayList(Robot),
    moves: usize,

    fn init(allocator: Allocator, x: i64, y: i64) Grid {
        return .{
            .allocator = allocator,
            .x = x,
            .y = y,
            .robots = std.ArrayList(Robot).init(allocator),
            .moves = 0,
        };
    }

    fn add(self: *Grid, robot: Robot) !void {
        try self.robots.append(robot);
    }

    fn move(self: *Grid) void {
        self.moves += 1;
        for (self.robots.items) |*robot| {
            robot.move(self.x, self.y);
        }
    }

    fn safety(self: Grid) usize {
        var counts: [4]usize = .{ 0, 0, 0, 0 };
        for (self.robots.items) |robot| {
            if (robot.quadrant(self.x, self.y)) |quadrant| {
                counts[quadrant] += 1;
            }
        }
        return counts[0] * counts[1] * counts[2] * counts[3];
    }

    fn connected(self: Grid) !bool {
        var points = Set(Point).init(self.allocator);
        defer points.deinit();
        for (self.robots.items) |robot| {
            const point = robot.position;
            if (points.contains(point)) {
                return false;
            }
            try points.add(point);
        }
        return true;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const lines = try Reader.init(allocator).stringLines();
    var robots = Grid.init(allocator, 101, 103);
    for (lines.items) |line| {
        const robot = try Robot.init(line);
        try robots.add(robot);
    }
    answer.part1(usize, 224357412, runFor(&robots, 100));
    answer.part2(usize, 7083, try runUntil(&robots));
}

fn runFor(robots: *Grid, seconds: usize) usize {
    for (0..seconds) |_| {
        robots.move();
    }
    return robots.safety();
}

fn runUntil(robots: *Grid) !usize {
    while (!(try robots.connected())) {
        robots.move();
    }
    return robots.moves;
}
