const std = @import("std");

pub const Context = struct {
    arena: std.heap.ArenaAllocator,

    pub fn init() Context {
        return .{
            .arena = std.heap.ArenaAllocator.init(std.heap.page_allocator),
        };
    }

    pub fn allocator(self: *Context) std.mem.Allocator {
        return self.arena.allocator();
    }

    pub fn deinit(self: *Context) void {
        self.arena.deinit();
    }
};
