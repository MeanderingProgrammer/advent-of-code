let non_empty s = String.length (String.trim s) != 0

(* 79 14 55 13 *)
let parse_numbers s =
  let numbers = String.split_on_char ' ' s in
  List.map int_of_string (List.filter non_empty numbers)

(* seeds: <numbers> *)
let parse_seeds s =
  match String.split_on_char ':' s with
  | _ :: numbers :: _ -> parse_numbers numbers
  | _ -> raise (Invalid_argument s)

type range_offset = { first : int; last : int; offset : int }

let rec update_offsets offsets first last offset =
  match offsets with
  | x :: xs ->
      let value, next_first =
        if first >= last || x.first > last || x.last < first then ([ x ], first)
        else
          let before =
            if x.first < first then
              [ { first = x.first; last = first - 1; offset = x.offset } ]
            else []
          in
          let overlap =
            [
              { first; last = Int.min x.last last; offset = offset + x.offset };
            ]
          in
          let after =
            if x.last > last then
              [ { first = last + 1; last = x.last; offset = x.offset } ]
            else []
          in
          ( before @ overlap @ after,
            if x.last == Int.max_int then x.last else x.last + 1 )
      in
      value @ update_offsets xs next_first last offset
  | [] -> []

let add_conversion offsets conversion =
  match parse_numbers conversion with
  | destination :: source :: length :: _ ->
      let offset = destination - source in
      update_offsets offsets source (source + length - 1) offset
  | _ -> raise (Invalid_argument conversion)

let rec add_conversions offsets conversions =
  match conversions with
  | x :: xs -> add_conversions (add_conversion offsets x) xs
  | _ -> offsets

let group_offsets group =
  let initial_offsets =
    [ { first = Int.min_int; last = Int.max_int; offset = 0 } ]
  in
  let conversions = List.tl group in
  add_conversions initial_offsets conversions

let rec groups_offsets groups =
  match groups with
  | x :: xs ->
      let offsets = group_offsets x in
      offsets :: groups_offsets xs
  | [] -> []

let rec find offset value =
  match offset with
  | x :: xs ->
      if value <= x.last && value >= x.first then value + x.offset
      else find xs value
  | _ -> raise (Invalid_argument "Could not find")

let rec apply offsets value =
  match offsets with
  | x :: xs ->
      let next_value = find x value in
      apply xs next_value
  | [] -> value

let get_min locations =
  List.fold_left Int.min (List.hd locations) (List.tl locations)

let rec get_seed_pairs seeds =
  match seeds with
  | start :: length :: xs ->
      let pair = List.init length (fun i -> start + i) in
      pair @ get_seed_pairs xs
  | _ -> []

let () =
  let groups = Aoc.Reader.read_groups () in
  let seeds = parse_seeds (List.nth (List.nth groups 0) 0) in
  let offsets = groups_offsets (List.tl groups) in
  let part1 = get_min (List.map (apply offsets) seeds) in
  let part2 = get_min (List.map (apply offsets) (get_seed_pairs seeds)) in
  Aoc.Answer.part1 621354867 part1 string_of_int;
  Aoc.Answer.part2 1 part2 string_of_int
