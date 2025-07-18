const std = @import("std");
const Allocator = std.mem.Allocator;
const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;

const Disk = std.ArrayList(usize);
const Files = std.ArrayList(File);

const File = struct {
    id: usize,
    size: usize,
    free: usize,
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution(allocator: Allocator) !void {
    const data = try Reader.init(allocator).ints();
    const files = try getFiles(allocator, data);
    answer.part1(usize, 6386640365805, checksum(try part1(allocator, files)));
    answer.part2(usize, 6423258376982, checksum(try part2(allocator, files)));
}

fn getFiles(allocator: Allocator, data: Disk) !Files {
    var result = Files.init(allocator);
    var i: usize = 0;
    while (i < data.items.len) : (i += 2) {
        const file = File{
            .id = i / 2,
            .size = data.items[i],
            .free = if ((i + 1) < data.items.len) data.items[i + 1] else 0,
        };
        try result.append(file);
    }
    return result;
}

fn part1(allocator: Allocator, input: Files) !Disk {
    var files = try input.clone();
    var i: usize = 0;
    var result = Disk.init(allocator);
    while (i < files.items.len) : (i += 1) {
        const file = files.items[i];
        try result.appendNTimes(file.id, file.size);
        for (0..file.free) |_| {
            var last = &files.items[files.items.len - 1];
            if (file.id != last.id) {
                try result.append(last.id);
                last.size -= 1;
                if (last.size == 0) {
                    _ = files.pop();
                }
            }
        }
    }
    return result;
}

fn part2(allocator: Allocator, input: Files) !Disk {
    var files = try input.clone();
    for (0..files.items.len) |i| {
        const id = files.items.len - (i + 1);
        const index = idToIndex(files, id).?;
        if (firstFit(files, index)) |location| {
            var file = files.orderedRemove(index);
            var before = &files.items[index - 1];
            var new_before = &files.items[location];
            before.free = before.free + file.size + file.free;
            file.free = new_before.free - file.size;
            new_before.free = 0;
            try files.insert(location + 1, file);
        }
    }
    var result = Disk.init(allocator);
    for (files.items) |file| {
        try result.appendNTimes(file.id, file.size);
        try result.appendNTimes(0, file.free);
    }
    return result;
}

fn idToIndex(files: Files, id: usize) ?usize {
    for (files.items, 0..) |file, i| {
        if (file.id == id) {
            return i;
        }
    }
    return null;
}

fn firstFit(files: Files, index: usize) ?usize {
    for (0..index) |i| {
        if (files.items[i].free >= files.items[index].size) {
            return i;
        }
    }
    return null;
}

fn checksum(disk: Disk) usize {
    var result: usize = 0;
    for (disk.items, 0..) |id, position| {
        result += (id * position);
    }
    return result;
}
