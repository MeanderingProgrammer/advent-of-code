const std = @import("std");

const Solutions = [_]struct { []const u8, []const u8 }{
    .{ "2021", "01" },
    .{ "2024", "01" },
    .{ "2024", "02" },
    .{ "2024", "03" },
    .{ "2024", "04" },
    .{ "2024", "05" },
    .{ "2024", "06" },
    .{ "2024", "07" },
    .{ "2024", "08" },
    .{ "2024", "09" },
    .{ "2024", "10" },
    .{ "2024", "11" },
};

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const lib = b.addModule("aoc", .{
        .root_source_file = b.path("commons/zig/mod.zig"),
        .target = target,
        .optimize = optimize,
    });

    inline for (Solutions) |solution| {
        const year = solution[0];
        const day = solution[1];
        const exe = b.addExecutable(.{
            .name = year ++ "_" ++ day,
            .root_source_file = b.path(year ++ "/" ++ day ++ "/solver.zig"),
            .target = target,
            .optimize = optimize,
        });
        exe.root_module.addImport("aoc", lib);
        b.installArtifact(exe);
        const run_exe = b.addRunArtifact(exe);
        if (b.args) |args| {
            run_exe.addArgs(args);
        }
        const run_step = b.step(exe.name, "Run " ++ year ++ " " ++ day);
        run_step.dependOn(&run_exe.step);
    }
}
