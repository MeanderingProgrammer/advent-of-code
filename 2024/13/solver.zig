const aoc = @import("aoc");
const answer = aoc.answer;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

pub const Machine = struct {
    a: Point,
    b: Point,
    prize: Point,

    fn init(lines: std.ArrayList([]const u8)) !Machine {
        return Machine{
            // Button A: X+94, Y+34
            .a = try parse_point(lines.items[0]),
            // Button B: X+22, Y+67
            .b = try parse_point(lines.items[1]),
            // Prize: X=8400, Y=5400
            .prize = try parse_point(lines.items[2]),
        };
    }

    fn parse_point(line: []const u8) !Point {
        var label_point = std.mem.splitBackwardsScalar(u8, line, ':');
        const point_section = label_point.first();
        var point_parts = std.mem.splitScalar(u8, point_section, ',');
        const x = try parse_coord(point_parts.next().?);
        const y = try parse_coord(point_parts.next().?);
        return Point.init(x, y);
    }

    fn parse_coord(part: []const u8) !i64 {
        var it = std.mem.splitBackwardsAny(u8, part, "+=");
        const value = it.first();
        return try std.fmt.parseInt(i64, value, 10);
    }

    fn tokens(self: Machine, offset: i64) i64 {
        // X1a + X2b = PX
        // Y1a + Y2b = PY -> a = (PY/Y1) - (Y2b/Y1)
        // X1((PY/Y1) - (Y2b/Y1)) + X2b = PX
        // (X1*PY/Y1) - (X1*Y2/Y1) + X2b = PX
        // (X2 - (X1*Y2/Y1))b = PX - (X1*PY/Y1)
        // ((X2*Y1-X1*Y2)/Y1)b = (PX*Y1-X1*PY)/Y1
        // b = ((PX*Y1-X1*PY)/Y1)/((X2*Y1-X1*Y2/Y1)
        // b = (PX*Y1-X1*PY)/(X2*Y1-X1*Y2)
        // a = (PX - X2b)/X1

        const x1: f64 = @floatFromInt(self.a.x);
        const x2: f64 = @floatFromInt(self.b.x);
        const px: f64 = @floatFromInt(self.prize.x + offset);
        const y1: f64 = @floatFromInt(self.a.y);
        const y2: f64 = @floatFromInt(self.b.y);
        const py: f64 = @floatFromInt(self.prize.y + offset);

        const bf = ((px * y1) - (x1 * py)) / ((x2 * y1) - (x1 * y2));
        const af = (px - (x2 * bf)) / x1;
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

fn solution() !void {
    const groups = try Reader.init().groups();
    var machines = std.ArrayList(Machine).init(allocator);
    for (groups.items) |lines| {
        try machines.append(try Machine.init(lines));
    }
    answer.part1(i64, 28138, total_tokens(machines, 0));
    answer.part2(i64, 108394825772874, total_tokens(machines, 10000000000000));
}

fn total_tokens(machines: std.ArrayList(Machine), offset: i64) i64 {
    var result: i64 = 0;
    for (machines.items) |machine| {
        const tokens = machine.tokens(offset);
        result += tokens;
    }
    return result;
}
