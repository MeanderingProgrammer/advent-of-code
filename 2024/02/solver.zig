const aoc = @import("aoc");
const std = @import("std");
const allocator = std.heap.page_allocator;

const Report = struct {
    levels: std.ArrayList(usize),

    fn init(line: []const u8) !Report {
        var levels = std.ArrayList(usize).init(allocator);
        var it = std.mem.tokenizeScalar(u8, line, ' ');
        while (it.next()) |item| {
            try levels.append(try std.fmt.parseInt(usize, item, 10));
        }
        return Report{ .levels = levels };
    }

    fn safe(self: Report, tolerant: bool) bool {
        if (check_levels(self.levels.items)) |index| {
            return tolerant and (self.safe_around(index) catch false);
        } else {
            return true;
        }
    }

    fn safe_around(self: Report, index: isize) !bool {
        const start = @as(usize, @intCast(@max(index - 1, 0)));
        const end = @min(@as(usize, @intCast(index + 2)), self.levels.items.len);
        for (start..end) |i| {
            var clone = try self.levels.clone();
            _ = clone.orderedRemove(i);
            if (check_levels(clone.items) == null) {
                return true;
            }
        }
        return false;
    }

    fn check_levels(levels: []usize) ?isize {
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
    try aoc.answer.timer(solution);
}

fn solution() !void {
    const reports = try aoc.reader.Reader.init().read(Report, Report.init);
    aoc.answer.part1(402, count_safe(reports, false));
    aoc.answer.part2(455, count_safe(reports, true));
}

fn count_safe(reports: std.ArrayList(Report), tolerant: bool) usize {
    var result: usize = 0;
    for (reports.items) |report| {
        result += if (report.safe(tolerant)) 1 else 0;
    }
    return result;
}
