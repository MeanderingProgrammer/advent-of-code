const std = @import("std");

pub fn Set(comptime T: type) type {
    const Map = std.AutoHashMap(T, void);
    return struct {
        map: Map,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator) Self {
            return .{ .map = Map.init(allocator) };
        }

        pub fn deinit(self: *Self) void {
            self.map.deinit();
        }

        pub fn clear(self: *Self) void {
            self.map.clearRetainingCapacity();
        }

        pub fn clone(self: Self) !Self {
            const map = try self.map.clone();
            return .{ .map = map };
        }

        pub fn add(self: *Self, value: T) !void {
            try self.map.put(value, {});
        }

        pub fn extend(self: *Self, other: Self) !void {
            var it = other.iterator();
            while (it.next()) |value| {
                try self.add(value.*);
            }
        }

        pub fn contains(self: Self, value: T) bool {
            return self.map.contains(value);
        }

        pub fn size(self: Self) usize {
            return self.map.count();
        }

        pub fn iterator(self: Self) Map.KeyIterator {
            return self.map.keyIterator();
        }
    };
}
