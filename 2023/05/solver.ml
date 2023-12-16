open Core

let non_empty s = not (String.is_empty (String.strip s))

(* 79 14 55 13 *)
let parse_numbers s =
  let numbers = String.split ~on:' ' s in
  List.map ~f:int_of_string (List.filter ~f:non_empty numbers)

(* seeds: <numbers> *)
let parse_seeds s =
  match String.split ~on:':' s with
  | [ _; numbers ] -> parse_numbers numbers
  | _ -> raise (Invalid_argument s)

type range = { first : int; last : int; offset : int }

let add_conversion offsets conversion =
  match parse_numbers conversion with
  | [ destination; source; length ] ->
      let offset = destination - source in
      { first = source; last = source + length - 1; offset } :: offsets
  | _ -> raise (Invalid_argument conversion)

let rec add_conversions offsets conversions =
  match conversions with
  | x :: xs -> add_conversions (add_conversion offsets x) xs
  | [] -> offsets

let rec group_offsets groups =
  match groups with
  | x :: xs ->
      let offsets = add_conversions [] (List.tl_exn x) in
      offsets :: group_offsets xs
  | [] -> []

let adjust_range r =
  { first = r.first + r.offset; last = r.last + r.offset; offset = r.offset }

let get_first r = r.first
let get_last r = r.last

let rec map_range offset r new_ranges =
  match offset with
  | x :: xs ->
      let split_ranges =
        if x.last >= r.first && x.first <= r.last then
          let first = Int.max x.first r.first in
          let last = Int.min x.last r.last in
          [ { first; last; offset = x.offset } ]
        else []
      in
      map_range xs r (split_ranges @ new_ranges)
  | [] ->
      if List.is_empty new_ranges then [ r ]
      else
        let ranges = List.map ~f:adjust_range new_ranges in
        let min_consumed = Aoc.Util.min (List.map ~f:get_first new_ranges) in
        let min_range =
          { first = r.first; last = min_consumed - 1; offset = 0 }
        in
        let max_consumed = Aoc.Util.max (List.map ~f:get_last new_ranges) in
        let max_range =
          { first = max_consumed + 1; last = r.last; offset = 0 }
        in
        if
          (not (Int.equal r.first min_consumed))
          && not (Int.equal r.last max_consumed)
        then min_range :: max_range :: ranges
        else if not (Int.equal r.first min_consumed) then min_range :: ranges
        else if not (Int.equal r.last max_consumed) then max_range :: ranges
        else ranges

let rec map_ranges offset ranges =
  match ranges with
  | x :: xs -> map_range offset x [] @ map_ranges offset xs
  | [] -> ranges

let rec apply offsets ranges =
  match offsets with
  | x :: xs -> apply xs (map_ranges x ranges)
  | [] -> Aoc.Util.min (List.map ~f:get_first ranges)

let rec seed_ranges seeds =
  match seeds with
  | x :: xs -> { first = x; last = x; offset = 0 } :: seed_ranges xs
  | _ -> []

let rec get_seeds seeds =
  match seeds with
  | first :: length :: xs ->
      { first; last = first + length - 1; offset = 0 } :: get_seeds xs
  | _ -> []

let () =
  let groups = Aoc.Reader.read_groups () in
  let seeds = parse_seeds (List.nth_exn (List.nth_exn groups 0) 0) in
  let offsets = group_offsets (List.tl_exn groups) in
  let part1 = (apply offsets) (seed_ranges seeds) in
  let part2 = (apply offsets) (get_seeds seeds) in
  Aoc.Answer.part1 621354867 part1 string_of_int;
  Aoc.Answer.part2 15880236 part2 string_of_int
