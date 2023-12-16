type row = { springs : char list; groups : int list }

(* 1,1,3 *)
let parse_groups s = List.map int_of_string (String.split_on_char ',' s)

(* ???.### <groups> *)
let parse_row s =
  match String.split_on_char ' ' s with
  | [ springs; groups ] ->
      {
        springs = springs |> String.to_seq |> List.of_seq;
        groups = parse_groups groups;
      }
  | _ -> raise (Invalid_argument s)

let group_fits springs group =
  if List.length springs < group then false
  else if
    List.exists (Char.equal '.') (List.filteri (fun i _ -> i < group) springs)
  then false
  else if List.length springs > group && List.nth springs group == '#' then
    false
  else true

let rec count springs groups cache =
  let handle_empty () = count (List.tl springs) groups cache in
  let handle_group group =
    match group_fits springs group with
    | false -> 0
    | true ->
        let next_springs = List.filteri (fun i _ -> i > group) springs in
        count next_springs (List.tl groups) cache
  in
  match List.assoc_opt (springs, groups) !cache with
  | Some value -> value
  | None ->
      let value =
        match springs with
        | [] -> if List.length groups == 0 then 1 else 0
        | spring :: _ -> (
            match groups with
            | [] -> if List.exists (Char.equal '#') springs then 0 else 1
            | group :: _ -> (
                match spring with
                | '.' -> handle_empty ()
                | '#' -> handle_group group
                | '?' -> handle_empty () + handle_group group
                | _ -> raise (Invalid_argument (String.make 1 spring))))
      in
      cache := ((springs, groups), value) :: !cache;
      value

let count_folded r = count r.springs r.groups (ref [])

let count_unfolded r =
  let rec repeat values n =
    match n with 0 -> [] | _ -> values @ repeat values (n - 1)
  in
  let springs = List.tl (repeat ([ '?' ] @ r.springs) 5) in
  let groups = repeat r.groups 5 in
  count springs groups (ref [])

let () =
  let values = Aoc.Reader.read_lines () in
  let rows = List.map parse_row values in
  let part1 = List.fold_left ( + ) 0 (List.map count_folded rows) in
  let part2 = List.fold_left ( + ) 0 (List.map count_unfolded rows) in
  Aoc.Answer.part1 8075 part1 string_of_int;
  Aoc.Answer.part2 4232520187524 part2 string_of_int
