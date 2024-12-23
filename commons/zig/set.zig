const std = @import("std");

pub fn Set(comptime T: type) type {
    const Map = comptime switch (@typeInfo(T)) {
        .Pointer => std.StringHashMap(void),
        else => std.AutoHashMap(T, void),
    };
    return struct {
        allocator: std.mem.Allocator,
        map: Map,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator) Self {
            return .{ .allocator = allocator, .map = Map.init(allocator) };
        }

        pub fn deinit(self: *Self) void {
            self.map.deinit();
        }

        pub fn clear(self: *Self) void {
            self.map.clearRetainingCapacity();
        }

        pub fn clone(self: Self) !Self {
            const map = try self.map.clone();
            return .{ .allocator = self.allocator, .map = map };
        }

        pub fn add(self: *Self, value: T) !void {
            try self.map.put(value, {});
        }

        pub fn remove(self: *Self, value: T) void {
            _ = self.map.remove(value);
        }

        pub fn intersection(self: Self, other: Self) !Self {
            var result = init(self.allocator);
            var it = self.iterator();
            while (it.next()) |value| {
                if (other.contains(value.*)) {
                    try result.add(value.*);
                }
            }
            return result;
        }

        pub fn extend(self: *Self, other: Self) !void {
            var it = other.iterator();
            while (it.next()) |value| {
                try self.add(value.*);
            }
        }

        pub fn difference(self: *Self, other: Self) void {
            var it = other.iterator();
            while (it.next()) |value| {
                self.remove(value.*);
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

        pub fn next(self: Self) T {
            var it = self.iterator();
            return it.next().?.*;
        }

        pub fn list(self: Self) !std.ArrayList(T) {
            var result = std.ArrayList(T).init(self.allocator);
            var it = self.iterator();
            while (it.next()) |value| {
                try result.append(value.*);
            }
            return result;
        }
    };
}
