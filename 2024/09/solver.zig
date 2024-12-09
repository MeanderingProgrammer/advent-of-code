const aoc = @import("aoc");
const answer = aoc.answer;
const Reader = aoc.reader.Reader;
const std = @import("std");
const allocator = std.heap.page_allocator;

const Disk = std.ArrayList(usize);
const Files = std.ArrayList(File);
const File = struct {
    id: usize,
    index: usize,
    size: usize,
    free: usize,
};

pub fn main() !void {
    try answer.timer(solution);
}

fn solution() !void {
    const data = try Reader.init().ints();
    const files = try get_files(data);
    answer.part1(usize, 6386640365805, checksum(try part1(files)));
    answer.part2(usize, 6423258376982, checksum(try part2(files)));
}

fn get_files(data: Disk) !Files {
    var result = Files.init(allocator);
    var i: usize = 0;
    var index: usize = 0;
    while (i < data.items.len) {
        const file = File{
            .id = (i / 2) + 1,
            .index = index,
            .size = data.items[i],
            .free = if ((i + 1) < data.items.len) data.items[i + 1] else 0,
        };
        try result.append(file);
        i += 2;
        index += (file.size + file.free);
    }
    return result;
}

fn part1(input: Files) !Disk {
    var files = try input.clone();
    var i: usize = 0;
    var result = Disk.init(allocator);
    while (i < files.items.len) {
        const file = files.items[i];
        for (0..file.size) |_| {
            try result.append(file.id);
        }
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
        i += 1;
    }
    return result;
}

fn part2(input: Files) !Disk {
    const files = try input.clone();
    const result = try initialize_disk(files);
    for (0..files.items.len) |i| {
        const index = files.items.len - (i + 1);
        const file = files.items[index];
        if (find_free(result, file)) |location| {
            for (location..(location + file.size)) |j| {
                result.items[j] = file.id;
            }
            for (file.index..(file.index + file.size)) |j| {
                result.items[j] = 0;
            }
        }
    }
    return result;
}

fn initialize_disk(files: Files) !Disk {
    var result = Disk.init(allocator);
    for (files.items) |file| {
        for (0..file.size) |_| {
            try result.append(file.id);
        }
        for (0..file.free) |_| {
            try result.append(0);
        }
    }
    return result;
}

fn find_free(disk: Disk, file: File) ?usize {
    for (0..file.index) |i| {
        if (all_free(disk, file, i)) {
            return i;
        }
    }
    return null;
}

fn all_free(disk: Disk, file: File, start: usize) bool {
    for (start..(start + file.size)) |i| {
        if (disk.items[i] != 0) {
            return false;
        }
    }
    return true;
}

fn checksum(disk: Disk) usize {
    var result: usize = 0;
    for (disk.items, 0..) |id, position| {
        if (id > 1) {
            result += ((id - 1) * position);
        }
    }
    return result;
}
