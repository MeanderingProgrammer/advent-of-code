const std = @import("std");

const aoc = @import("aoc");
const answer = aoc.answer;

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(c: *aoc.Context) !void {
    const grid = try aoc.Reader.init(c.allocator()).grid();
    answer.part1(usize, 2543, part1(grid));
    answer.part2(usize, 1930, part2(grid));
}

fn part1(grid: aoc.Grid(u8)) usize {
    var result: usize = 0;
    var points = grid.points();
    while (points.next()) |point| {
        inline for (std.meta.fields(aoc.Heading)) |heading| {
            const contains = has(grid, point.*, @enumFromInt(heading.value), "XMAS");
            result += if (contains) 1 else 0;
        }
    }
    return result;
}

fn part2(grid: aoc.Grid(u8)) usize {
    var result: usize = 0;
    var points = grid.points();
    while (points.next()) |p1| {
        const p2 = p1.plus(aoc.Heading.s.point().times(2));
        const sw = mas(grid, p1.*, aoc.Heading.sw);
        const nw = mas(grid, p2, aoc.Heading.nw);
        result += if (sw and nw) 1 else 0;
    }
    return result;
}

fn mas(grid: aoc.Grid(u8), start: aoc.Point, heading: aoc.Heading) bool {
    return has(grid, start, heading, "MAS") or has(grid, start, heading, "SAM");
}

fn has(grid: aoc.Grid(u8), start: aoc.Point, heading: aoc.Heading, goal: []const u8) bool {
    var point = start;
    for (goal) |ch| {
        const matches = if (grid.get(point)) |value| ch == value else false;
        if (!matches) {
            return false;
        }
        point = point.plus(heading.point());
    }
    return true;
}
