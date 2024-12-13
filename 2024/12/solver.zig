const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Heading = aoc.point.Heading;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Points = std.AutoHashMap(Point, bool);
const Region = struct {
    plant: u8,
    points: Points,

    fn init(plant: u8) Region {
        return Region{
            .plant = plant,
            .points = Points.init(allocator),
        };
    }

    fn add(self: *Region, point: Point) !void {
        try self.points.put(point, true);
    }

    fn price(self: Region, bulk: bool) usize {
        const area: usize = self.points.count();
        return area * if (bulk) self.sides() else self.perimeter();
    }

    fn sides(self: Region) usize {
        var corners: usize = 0;
        var points = self.points.keyIterator();
        while (points.next()) |point| {
            if (self.neighbors(point) == 4) {
                continue;
            }
            corners += self.outer(point, Heading.n);
            corners += self.outer(point, Heading.e);
            corners += self.outer(point, Heading.s);
            corners += self.outer(point, Heading.w);
            corners += self.inner(point, Heading.n, Heading.nw);
            corners += self.inner(point, Heading.n, Heading.ne);
            corners += self.inner(point, Heading.s, Heading.sw);
            corners += self.inner(point, Heading.s, Heading.se);
        }
        return corners;
    }

    fn outer(self: Region, point: *Point, start: Heading) usize {
        var heading = start;
        for (0..3) |_| {
            if (self.has(point, heading)) {
                return 0;
            }
            heading = heading.clockwise();
        }
        return 1;
    }

    fn inner(self: Region, point: *Point, gap: Heading, edge: Heading) usize {
        return if (!self.has(point, gap) and self.has(point, edge)) 1 else 0;
    }

    fn has(self: Region, point: *Point, heading: Heading) bool {
        return self.points.contains(point.plus(heading.point()));
    }

    fn perimeter(self: Region) usize {
        var result: usize = 0;
        var points = self.points.keyIterator();
        while (points.next()) |point| {
            result += (4 - self.neighbors(point));
        }
        return result;
    }

    fn neighbors(self: Region, point: *Point) usize {
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

fn solution() !void {
    const grid = try Reader.init().grid();
    const regions = try split_regions(grid);
    answer.part1(usize, 1451030, total(regions, false));
    answer.part2(usize, 859494, total(regions, true));
}

fn split_regions(grid: Grid) !std.ArrayList(Region) {
    var regions = std.ArrayList(Region).init(allocator);
    var seen = Points.init(allocator);
    var points = grid.points();
    while (points.next()) |p| {
        const point = p.*;
        if (seen.contains(point)) {
            continue;
        }
        var region = Region.init(grid.get(point).?);
        var queue = std.ArrayList(Point).init(allocator);
        try queue.append(point);
        while (queue.items.len > 0) {
            const current = queue.pop();
            if (seen.contains(current)) {
                continue;
            }
            try seen.put(current, true);
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

fn total(regions: std.ArrayList(Region), bulk: bool) usize {
    var result: usize = 0;
    for (regions.items) |region| {
        result += region.price(bulk);
    }
    return result;
}
