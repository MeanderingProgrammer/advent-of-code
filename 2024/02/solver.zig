const std = @import("std");
const aoc = @import("aoc");
const answer = aoc.answer;

const Report = struct {
    levels: std.ArrayList(usize),

    fn init(allocator: std.mem.Allocator, line: []const u8) !Report {
        var levels = std.ArrayList(usize).init(allocator);
        var it = std.mem.tokenizeScalar(u8, line, ' ');
        while (it.next()) |item| {
            try levels.append(try aoc.util.decimal(usize, item));
        }
        return .{
            .levels = levels,
        };
    }

    fn safe(self: Report, tolerant: bool) bool {
        if (checkLevels(self.levels.items)) |index| {
            return tolerant and (self.safeAround(index) catch false);
        } else {
            return true;
        }
    }

    fn safeAround(self: Report, index: isize) !bool {
        const start = @as(usize, @intCast(@max(index - 1, 0)));
        const end = @min(@as(usize, @intCast(index + 2)), self.levels.items.len);
        for (start..end) |i| {
            var clone = try self.levels.clone();
            _ = clone.orderedRemove(i);
            if (checkLevels(clone.items) == null) {
                return true;
            }
        }
        return false;
    }

    fn checkLevels(levels: []usize) ?isize {
        const increasing = levels[0] < levels[1];
        for (0..levels.len - 1) |i| {
            const l1 = levels[i];
            const l2 = levels[i + 1];
            if (increasing != (l1 < l2)) {
                return @intCast(i);
            }
            const differnce = if (increasing) l2 - l1 else l1 - l2;
            if (differnce < 1 or differnce > 3) {
                return @intCast(i);
            }
        }
        return null;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const reports = try aoc.Reader.init(c.allocator()).lines(Report, Report.init);
    answer.part1(usize, 402, countSafe(reports, false));
    answer.part2(usize, 455, countSafe(reports, true));
}

fn countSafe(reports: std.ArrayList(Report), tolerant: bool) usize {
    var result: usize = 0;
    for (reports.items) |report| {
        result += if (report.safe(tolerant)) 1 else 0;
    }
    return result;
}
