const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Equation = struct {
    target: usize,
    values: std.ArrayList(usize),

    fn init(line: []const u8) !Equation {
        var it = std.mem.splitSequence(u8, line, ": ");
        const target = try to_int(it.next().?);
        var values = std.ArrayList(usize).init(allocator);
        var values_it = std.mem.splitScalar(u8, it.next().?, ' ');
        while (values_it.next()) |value| {
            try values.append(try to_int(value));
        }
        return Equation{ .target = target, .values = values };
    }

    fn valid(self: Equation, concat: bool) !bool {
        var values = std.ArrayList(usize).init(allocator);
        defer values.deinit();
        try values.append(self.values.items[0]);
        for (1..self.values.items.len) |i| {
            const value = self.values.items[i];
            for (0..values.items.len) |j| {
                const current = values.items[j];
                values.items[j] = current + value;
                const multiplied = current * value;
                if (multiplied <= self.target) {
                    try values.append(multiplied);
                }
                if (concat) {
                    const digits = std.math.log10(value) + 1;
                    const concated = current * std.math.pow(usize, 10, digits) + value;
                    if (concated <= self.target) {
                        try values.append(concated);
                    }
                }
            }
        }
        return std.mem.containsAtLeast(usize, values.items, 1, &.{self.target});
    }

    fn to_int(s: []const u8) !usize {
        return std.fmt.parseInt(usize, s, 10);
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const equations = try Reader.init().lines(Equation, Equation.init);
    answer.part1(usize, 1289579105366, try calibration(equations, false));
    answer.part2(usize, 92148721834692, try calibration(equations, true));
}

fn calibration(equations: std.ArrayList(Equation), concat: bool) !usize {
    var result: usize = 0;
    for (equations.items) |equation| {
        result += if (try equation.valid(concat)) equation.target else 0;
    }
    return result;
}
