const std = @import("std");
const Point = @import("point.zig").Point;
const allocator = std.heap.page_allocator;

const Map = std.AutoHashMap(Point, u8);

pub const Grid = struct {
    grid: Map,

    pub fn init(lines: std.ArrayList([]const u8)) !Grid {
        var grid = Map.init(allocator);
        for (lines.items, 0..) |line, y| {
            for (line, 0..) |value, x| {
                try grid.put(Point.init(@intCast(x), @intCast(y)), value);
            }
        }
        return Grid{ .grid = grid };
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
};
