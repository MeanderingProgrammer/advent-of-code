const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const Heading = aoc.point.Heading;
const Reader = aoc.reader.Reader;
const std = @import("std");

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const grid = try Reader.init().grid();
    answer.part1(usize, 2543, part1(grid));
    answer.part2(usize, 1930, part2(grid));
}

fn part1(grid: Grid) usize {
    var result: usize = 0;
    var points = grid.points();
    while (points.next()) |point| {
        inline for (std.meta.fields(Heading)) |heading| {
            const contains = has(grid, point, @enumFromInt(heading.value), "XMAS");
            result += if (contains) 1 else 0;
        }
    }
    return result;
}

fn part2(grid: Grid) usize {
    var result: usize = 0;
    var points = grid.points();
    while (points.next()) |point| {
        const sw = mas(grid, point, Heading.sw);
        const nw = mas(grid, &point.add(0, 2), Heading.nw);
        result += if (sw and nw) 1 else 0;
    }
    return result;
}

fn mas(grid: Grid, start: *const Point, heading: Heading) bool {
    return has(grid, start, heading, "MAS") or has(grid, start, heading, "SAM");
}

fn has(grid: Grid, start: *const Point, heading: Heading, goal: []const u8) bool {
    var point = start.*;
    for (goal) |ch| {
        const matches = if (grid.get(point)) |value| ch == value else false;
        if (!matches) {
            return false;
        }
        point = point.head(heading);
    }
    return true;
}
