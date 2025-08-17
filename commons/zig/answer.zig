const std = @import("std");
const Context = @import("context.zig").Context;

pub fn timer(solution: fn (*Context) anyerror!void) !void {
    var start = try std.time.Timer.start();
    var c = Context.init();
    defer c.deinit();
    try solution(&c);
    write("Runtime (ns): {}\n", .{start.read()});
}

pub fn part1(comptime T: type, expected: T, actual: T) void {
    part(1, T, expected, actual);
}

pub fn part2(comptime T: type, expected: T, actual: T) void {
    part(2, T, expected, actual);
}

fn part(n: usize, comptime T: type, expected: T, actual: T) void {
    const fmt = comptime switch (@typeInfo(T)) {
        .pointer => "{s}",
        else => "{any}",
    };
    const equal = switch (@typeInfo(T)) {
        .pointer => std.mem.eql(u8, expected, actual),
        else => expected == actual,
    };
    if (!equal) {
        const format = "Part {d} incorrect, expected " ++ fmt ++ " but got " ++ fmt;
        std.debug.panic(format, .{ n, expected, actual });
    }
    const format = "Part {d}: " ++ fmt ++ "\n";
    write(format, .{ n, actual });
}

fn write(comptime format: []const u8, args: anytype) void {
    std.io.getStdOut().writer().print(format, args) catch {};
}
