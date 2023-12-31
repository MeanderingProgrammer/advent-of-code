open Core

(* seeds: <numbers> *)
let parse_seeds s =
  match String.split ~on:':' s with
  | [ _; numbers ] -> Aoc.Util.parse_numbers numbers
  | _ -> raise (Invalid_argument s)

type range = { first : int; last : int; offset : int }

let parse_range s =
  match Aoc.Util.parse_numbers s with
  | [ destination; source; length ] ->
      {
        first = source;
        last = source + length - 1;
        offset = destination - source;
      }
  | _ -> raise (Invalid_argument s)

let rec parse_offset conversions =
  match conversions with
  | [] -> []
  | x :: xs -> parse_range x :: parse_offset xs

let rec parse_offsets groups =
  match groups with
  | [] -> []
  | x :: xs -> parse_offset (List.tl_exn x) :: parse_offsets xs

let adjust_range r =
  { first = r.first + r.offset; last = r.last + r.offset; offset = r.offset }

let rec map_range offset r new_ranges =
  match offset with
  | [] -> List.map ~f:adjust_range new_ranges
  | x :: xs ->
      let split_ranges =
        if x.last >= r.first && x.first <= r.last then
          let first = Int.max x.first r.first in
          let last = Int.min x.last r.last in
          [ { first; last; offset = x.offset } ]
        else []
      in
      map_range xs r (split_ranges @ new_ranges)

let rec map_ranges offset ranges =
  match ranges with
  | [] -> ranges
  | x :: xs -> map_range offset x [] @ map_ranges offset xs

let rec apply offsets ranges =
  match offsets with
  | [] -> Aoc.Util.min (List.map ~f:(fun r -> r.first) ranges)
  | x :: xs -> apply xs (map_ranges x ranges)

let rec seed_ranges seeds =
  match seeds with
  | [] -> []
  | x :: xs -> { first = x; last = x; offset = 0 } :: seed_ranges xs

let rec get_seeds seeds =
  match seeds with
  | first :: length :: xs ->
      { first; last = first + length - 1; offset = 0 } :: get_seeds xs
  | _ -> []

let () =
  let groups = Aoc.Reader.read_groups () in
  let seeds = parse_seeds (List.hd_exn (List.hd_exn groups)) in
  let offsets = parse_offsets (List.tl_exn groups) in
  let part1 = (apply offsets) (seed_ranges seeds) in
  let part2 = (apply offsets) (get_seeds seeds) in
  Aoc.Answer.part1 621354867 part1 string_of_int;
  Aoc.Answer.part2 15880236 part2 string_of_int
