open Core
open Printf

let () =
  let values = Aoc.Reader.read_lines () in
  printf "%s\n" (String.concat ~sep:"\n" values);
  Aoc.Answer.part1 1 1 string_of_int
