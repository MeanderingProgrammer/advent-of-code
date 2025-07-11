const Point = @import("point.zig").Point;
const std = @import("std");
const Allocator = std.mem.Allocator;

const Map = std.AutoHashMap(Point, u8);
pub const Grid = struct {
    allocator: Allocator,
    height: usize,
    width: usize,
    grid: Map,

    pub fn init(allocator: Allocator, lines: std.ArrayList([]const u8)) !Grid {
        var grid = Map.init(allocator);
        for (lines.items, 0..) |line, y| {
            for (line, 0..) |value, x| {
                const point = Point.init(@intCast(x), @intCast(y));
                try grid.put(point, value);
            }
        }
        return .{
            .allocator = allocator,
            .height = lines.items.len,
            .width = lines.items[0].len,
            .grid = grid,
        };
    }

    pub fn points(self: Grid) Map.KeyIterator {
        return self.grid.keyIterator();
    }

    pub fn get(self: Grid, point: Point) ?u8 {
        return self.grid.get(point);
    }

    pub fn set(self: *Grid, point: Point, value: u8) !void {
        try self.grid.put(point, value);
    }

    pub fn getValues(self: Grid, value: u8) !std.ArrayList(Point) {
        var result = std.ArrayList(Point).init(self.allocator);
        var it = self.grid.iterator();
        while (it.next()) |entry| {
            if (entry.value_ptr.* == value) {
                try result.append(entry.key_ptr.*);
            }
        }
        return result;
    }

    pub fn string(self: Grid) ![]const u8 {
        var result = std.ArrayList(u8).init(self.allocator);
        for (0..self.height) |y| {
            for (0..self.width) |x| {
                const point = Point.init(@intCast(x), @intCast(y));
                try result.append(self.get(point).?);
            }
            try result.append('\n');
        }
        return result.items;
    }
};
