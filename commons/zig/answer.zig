const std = @import("std");

pub fn timer(solution: fn () anyerror!void) !void {
    var start = try std.time.Timer.start();
    try solution();
    write("Runtime (ns): {}\n", .{start.read()});
}

pub fn part1(comptime T: type, expected: T, result: T) void {
    part(1, T, expected, result);
}

pub fn part2(comptime T: type, expected: T, result: T) void {
    part(2, T, expected, result);
}

fn part(n: usize, comptime T: type, expected: T, result: T) void {
    const fmt = comptime switch (@typeInfo(T)) {
        .pointer => "{s}",
        else => "{any}",
    };
    const equal = switch (@typeInfo(T)) {
        .pointer => std.mem.eql(u8, expected, result),
        else => expected == result,
    };
    if (!equal) {
        const format = "Part {d} incorrect, expected " ++ fmt ++ " but got " ++ fmt;
        std.debug.panic(format, .{ n, expected, result });
    }
    const format = "Part {d}: " ++ fmt ++ "\n";
    write(format, .{ n, result });
}

fn write(comptime format: []const u8, args: anytype) void {
    std.io.getStdOut().writer().print(format, args) catch {};
}
