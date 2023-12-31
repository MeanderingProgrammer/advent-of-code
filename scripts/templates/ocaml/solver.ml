open Aoc
open Core

let () =
  let values = Reader.read_lines () in
  printf "%s\n" (String.concat ~sep:"\n" values);
  Answer.part1 1 1 string_of_int
