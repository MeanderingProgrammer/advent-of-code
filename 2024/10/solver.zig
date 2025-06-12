const aoc = @import("aoc");
const answer = aoc.answer;
const Grid = aoc.grid.Grid;
const Point = aoc.point.Point;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Info = struct {
    score: usize,
    rating: usize,
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const grid = try Reader.init().grid();
    const heads = try grid.get_values('0');
    var info = Info{ .score = 0, .rating = 0 };
    for (heads.items) |head| {
        const head_info = try process(grid, head);
        info.score += head_info.score;
        info.rating += head_info.rating;
    }
    answer.part1(usize, 717, info.score);
    answer.part2(usize, 1686, info.rating);
}

fn process(grid: Grid, head: Point) !Info {
    var seen = std.AutoHashMap(Point, usize).init(allocator);
    var queue = std.ArrayList(Point).init(allocator);
    try queue.append(head);
    while (queue.items.len > 0) {
        const point = queue.pop().?;
        const count = if (seen.get(point)) |current| current else 0;
        try seen.put(point, count + 1);
        const value = grid.get(point).?;
        for (point.neighbors()) |next_point| {
            if (grid.get(next_point)) |next_value| {
                if ((value + 1) == next_value) {
                    try queue.append(next_point);
                }
            }
        }
    }
    var info = Info{ .score = 0, .rating = 0 };
    var it = seen.iterator();
    while (it.next()) |entry| {
        const point = entry.key_ptr.*;
        if (grid.get(point).? == '9') {
            info.score += 1;
            info.rating += entry.value_ptr.*;
        }
    }
    return info;
}
