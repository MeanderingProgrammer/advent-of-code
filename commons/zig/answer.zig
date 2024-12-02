const std = @import("std");

pub fn timer(solution: fn () anyerror!void) !void {
    var start = try std.time.Timer.start();
    try solution();
    write("Runtime (ns): {}\n", .{start.read()});
}

pub fn part1(expected: anytype, result: anytype) void {
    part(1, expected, result);
}

pub fn part2(expected: anytype, result: anytype) void {
    part(2, expected, result);
}

fn part(n: usize, expected: anytype, result: anytype) void {
    // TODO: Improve how strings are printed out
    if (expected != result) {
        std.debug.panic("Part {d} incorrect, expected {any} but got {any}", .{ n, expected, result });
    }
    write("Part {d}: {any}\n", .{ n, result });
}

fn write(comptime format: []const u8, args: anytype) void {
    std.io.getStdOut().writer().print(format, args) catch {};
}
