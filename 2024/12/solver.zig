const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.array_list.Managed;

const aoc = @import("aoc");
const answer = aoc.answer;

const Region = struct {
    plant: u8,
    points: aoc.Set(aoc.Point),

    fn init(allocator: Allocator, plant: u8) Region {
        return .{
            .plant = plant,
            .points = aoc.Set(aoc.Point).init(allocator),
        };
    }

    fn add(self: *Region, point: aoc.Point) !void {
        try self.points.add(point);
    }

    fn price(self: Region, bulk: bool) usize {
        const area: usize = self.points.size();
        return area * if (bulk) self.sides() else self.perimeter();
    }

    fn sides(self: Region) usize {
        var corners: usize = 0;
        var points = self.points.iterator();
        while (points.next()) |point| {
            if (self.neighbors(point) == 4) {
                continue;
            }
            corners += self.outer(point, aoc.Heading.n);
            corners += self.outer(point, aoc.Heading.e);
            corners += self.outer(point, aoc.Heading.s);
            corners += self.outer(point, aoc.Heading.w);
            corners += self.inner(point, aoc.Heading.n, aoc.Heading.nw);
            corners += self.inner(point, aoc.Heading.n, aoc.Heading.ne);
            corners += self.inner(point, aoc.Heading.s, aoc.Heading.sw);
            corners += self.inner(point, aoc.Heading.s, aoc.Heading.se);
        }
        return corners;
    }

    fn outer(self: Region, point: *aoc.Point, start: aoc.Heading) usize {
        var heading = start;
        for (0..3) |_| {
            if (self.has(point, heading)) {
                return 0;
            }
            heading = heading.right();
        }
        return 1;
    }

    fn inner(self: Region, point: *aoc.Point, gap: aoc.Heading, edge: aoc.Heading) usize {
        return if (!self.has(point, gap) and self.has(point, edge)) 1 else 0;
    }

    fn has(self: Region, point: *aoc.Point, heading: aoc.Heading) bool {
        return self.points.contains(point.plus(heading.point()));
    }

    fn perimeter(self: Region) usize {
        var result: usize = 0;
        var points = self.points.iterator();
        while (points.next()) |point| {
            result += (4 - self.neighbors(point));
        }
        return result;
    }

    fn neighbors(self: Region, point: *aoc.Point) usize {
        var result: usize = 0;
        for (point.neighbors()) |neighbor| {
            if (self.points.contains(neighbor)) {
                result += 1;
            }
        }
        return result;
    }
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const grid = try aoc.Reader.init(c.allocator()).grid();
    const regions = try splitRegions(c.allocator(), grid);
    answer.part1(usize, 1451030, total(regions, false));
    answer.part2(usize, 859494, total(regions, true));
}

fn splitRegions(allocator: Allocator, grid: aoc.Grid(u8)) !List(Region) {
    var regions = List(Region).init(allocator);
    var seen = aoc.Set(aoc.Point).init(allocator);
    var points = grid.points();
    while (points.next()) |p| {
        const point = p.*;
        if (seen.contains(point)) {
            continue;
        }
        var region = Region.init(allocator, grid.get(point).?);
        var queue = List(aoc.Point).init(allocator);
        try queue.append(point);
        while (queue.items.len > 0) {
            const current = queue.pop().?;
            if (seen.contains(current)) {
                continue;
            }
            try seen.add(current);
            try region.add(current);
            for (current.neighbors()) |next| {
                if (grid.get(next)) |plant| {
                    if (plant == region.plant) {
                        try queue.append(next);
                    }
                }
            }
        }
        try regions.append(region);
    }
    return regions;
}

fn total(regions: List(Region), bulk: bool) usize {
    var result: usize = 0;
    for (regions.items) |region| {
        result += region.price(bulk);
    }
    return result;
}
