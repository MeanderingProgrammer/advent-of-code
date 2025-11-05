const std = @import("std");

const Day = struct {
    year: []const u8,
    day: []const u8,
};

const Days = [_]Day{
    .{ .year = "2021", .day = "01" },
    .{ .year = "2024", .day = "01" },
    .{ .year = "2024", .day = "02" },
    .{ .year = "2024", .day = "03" },
    .{ .year = "2024", .day = "04" },
    .{ .year = "2024", .day = "05" },
    .{ .year = "2024", .day = "06" },
    .{ .year = "2024", .day = "07" },
    .{ .year = "2024", .day = "08" },
    .{ .year = "2024", .day = "09" },
    .{ .year = "2024", .day = "10" },
    .{ .year = "2024", .day = "11" },
    .{ .year = "2024", .day = "12" },
    .{ .year = "2024", .day = "13" },
    .{ .year = "2024", .day = "14" },
    .{ .year = "2024", .day = "15" },
    .{ .year = "2024", .day = "16" },
    .{ .year = "2024", .day = "17" },
    .{ .year = "2024", .day = "18" },
    .{ .year = "2024", .day = "19" },
    .{ .year = "2024", .day = "20" },
    .{ .year = "2024", .day = "21" },
    .{ .year = "2024", .day = "22" },
    .{ .year = "2024", .day = "23" },
    .{ .year = "2024", .day = "24" },
    .{ .year = "2024", .day = "25" },
};

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const lib = b.addModule("aoc", .{
        .root_source_file = b.path("commons/zig/mod.zig"),
        .target = target,
        .optimize = optimize,
    });

    const check_step = b.step("check", "Check if project compiles");

    inline for (Days) |day| {
        const name = day.year ++ "_" ++ day.day;
        const folder = day.year ++ "/" ++ day.day;
        const module = b.createModule(.{
            .root_source_file = b.path(folder ++ "/solver.zig"),
            .imports = &.{.{ .name = "aoc", .module = lib }},
            .target = target,
            .optimize = optimize,
        });

        const exe = b.addExecutable(.{
            .name = name,
            .root_module = module,
        });
        b.installArtifact(exe);
        const run = b.addRunArtifact(exe);
        if (b.args) |args| {
            run.addArgs(args);
        }
        b.step(name, "Run " ++ folder).dependOn(&run.step);

        const check = b.addExecutable(.{
            .name = name,
            .root_module = module,
        });
        check_step.dependOn(&check.step);
    }
}
