const aoc = @import("aoc");
const answer = aoc.answer;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const std = @import("std");
const Allocator = std.mem.Allocator;

pub const Machine = struct {
    a: Point,
    b: Point,
    prize: Point,

    fn init(lines: std.ArrayList([]const u8)) !Machine {
        return .{
            // Button A: X+94, Y+34
            .a = try parsePoint(lines.items[0]),
            // Button B: X+22, Y+67
            .b = try parsePoint(lines.items[1]),
            // Prize: X=8400, Y=5400
            .prize = try parsePoint(lines.items[2]),
        };
    }

    fn parsePoint(line: []const u8) !Point {
        var label_point = std.mem.splitBackwardsScalar(u8, line, ':');
        const point_section = label_point.first();
        var point_parts = std.mem.splitScalar(u8, point_section, ',');
        const x = try parseCoord(point_parts.next().?);
        const y = try parseCoord(point_parts.next().?);
        return Point.init(x, y);
    }

    fn parseCoord(part: []const u8) !i64 {
        var it = std.mem.splitBackwardsAny(u8, part, "+=");
        const value = it.first();
        return try std.fmt.parseInt(i64, value, 10);
    }

    fn tokens(self: Machine, offset: i64) i64 {
        // ax*a + bx*b = px
        // ay*a + by*b = py
        // Solution 1:
        // a = (py/ay) - (by*b/ay)
        // ax[(py/ay) - (by*b/ay)] + bx*b = px
        // (ax*py/ay) - (ax*by*b/ay) + bx*b = px
        // [bx - (ax*by/ay)]b = px - (ax*py/ay)
        // [(bx*ay-ax*by)/ay]b = (px*ay-ax*py)/ay
        // b = [(px*ay-ax*py)/ay]/[(bx*ay-ax*by/ay]
        // b = (px*ay-ax*py)/(bx*ay-ax*by)
        // Solution 2:
        // ax*a = px - bx*b
        // a = (px - bx*b)/ax

        const ax: f64 = @floatFromInt(self.a.x);
        const bx: f64 = @floatFromInt(self.b.x);
        const px: f64 = @floatFromInt(self.prize.x + offset);
        const ay: f64 = @floatFromInt(self.a.y);
        const by: f64 = @floatFromInt(self.b.y);
        const py: f64 = @floatFromInt(self.prize.y + offset);

        const bf = ((px * ay) - (ax * py)) / ((bx * ay) - (ax * by));
        const af = (px - (bx * bf)) / ax;
        const a: i64 = @intFromFloat(af);
        const b: i64 = @intFromFloat(bf);

        if (a < 0 or b < 0) {
            return 0;
        }
        if (self.a.x * a + self.b.x * b != self.prize.x + offset) {
            return 0;
        }
        if (self.a.y * a + self.b.y * b != self.prize.y + offset) {
            return 0;
        }
        return (3 * a) + b;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const groups = try Reader.init(allocator).groups();
    var machines = std.ArrayList(Machine).init(allocator);
    for (groups.items) |lines| {
        try machines.append(try Machine.init(lines));
    }
    answer.part1(i64, 28138, totalTokens(machines, 0));
    answer.part2(i64, 108394825772874, totalTokens(machines, 10000000000000));
}

fn totalTokens(machines: std.ArrayList(Machine), offset: i64) i64 {
    var result: i64 = 0;
    for (machines.items) |machine| {
        const tokens = machine.tokens(offset);
        result += tokens;
    }
    return result;
}
