const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Direction = aoc.point.Direction;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const State = struct {
    point: Point,
    direction: Direction,
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    var grid = try Reader.init().grid();
    const start = get_start(grid).?;
    var path = (try follow(&grid, start)).?;
    answer.part1(usize, 5516, path.count());
    answer.part2(usize, 2008, try obstacles(&grid, start, path));
}

fn get_start(grid: Grid) ?Point {
    var points = grid.points();
    while (points.next()) |point| {
        if (grid.get(point.*).? == '^') {
            return point.*;
        }
    }
    return null;
}

fn follow(grid: *Grid, start: Point) !?std.AutoHashMap(Point, bool) {
    var seen = std.AutoHashMap(State, bool).init(allocator);
    defer seen.deinit();
    var point = start;
    var direction = Direction.n;
    while (grid.get(point) != null) {
        const state = State{
            .point = point,
            .direction = direction,
        };
        if (seen.contains(state)) {
            return null;
        }
        try seen.put(state, true);
        const next_point = point.go(direction);
        if ((grid.get(next_point) orelse '.') == '#') {
            direction = direction.clockwise();
        } else {
            point = next_point;
        }
    }
    var points = std.AutoHashMap(Point, bool).init(allocator);
    var it = seen.keyIterator();
    while (it.next()) |state| {
        try points.put(state.point, true);
    }
    return points;
}

fn obstacles(grid: *Grid, start: Point, options: std.AutoHashMap(Point, bool)) !usize {
    var result: usize = 0;
    var it = options.keyIterator();
    while (it.next()) |point| {
        const p = point.*;
        if ((grid.get(p) orelse '#') != '^') {
            try grid.set(p, '#');
            if ((try follow(grid, start)) == null) {
                result += 1;
            }
            try grid.set(p, '.');
        }
    }
    return result;
}
