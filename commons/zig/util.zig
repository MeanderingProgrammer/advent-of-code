const std = @import("std");

pub fn decimal(comptime T: type, s: []const u8) !T {
    return std.fmt.parseInt(T, s, 10);
}
