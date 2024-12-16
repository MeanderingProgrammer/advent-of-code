const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Direction = aoc.point.Direction;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const Set = aoc.set.Set;
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
    const start = (try grid.get_values('^')).getLast();
    var path = (try follow(&grid, start)).?;
    answer.part1(usize, 5516, path.size());
    answer.part2(usize, 2008, try obstacles(&grid, start, path));
}

fn follow(grid: *Grid, start: Point) !?Set(Point) {
    var seen = Set(State).init(allocator);
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
        try seen.add(state);
        const next_point = point.plus(direction.point());
        if ((grid.get(next_point) orelse '.') == '#') {
            direction = direction.right();
        } else {
            point = next_point;
        }
    }
    var points = Set(Point).init(allocator);
    var it = seen.iterator();
    while (it.next()) |state| {
        try points.add(state.point);
    }
    return points;
}

fn obstacles(grid: *Grid, start: Point, options: Set(Point)) !usize {
    var result: usize = 0;
    var it = options.iterator();
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
