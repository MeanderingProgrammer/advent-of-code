open Aoc.Point

let get_max grid f =
  let points, _ = List.split grid in
  let values = List.map f points in
  List.fold_left Int.max (List.hd values) (List.tl values)

let get_range max inclusive =
  let offset = if inclusive then 1 else 0 in
  Seq.take (max + offset) (Seq.ints 0) |> List.of_seq

let rec differences grid range f src dst =
  match range with
  | [] -> 0
  | x :: xs ->
      let target_value = List.assoc (f src x) grid in
      let difference =
        match List.assoc_opt (f dst x) grid with
        | None -> 0
        | Some value -> if value == target_value then 0 else 1
      in
      difference + differences grid xs f src dst

let can_fold grid max f target line =
  let range = get_range max true in
  let before_line = get_range line true in
  let folded_over = List.map (fun i -> line + (line - i + 1)) before_line in
  let values = List.map2 (differences grid range f) before_line folded_over in
  let value = List.fold_left ( + ) 0 values in
  value == target

let sum values multiplier =
  List.fold_left ( + ) 0
    (List.map (fun value -> (value + 1) * multiplier) values)

let reflections target grid =
  let max_x = get_max grid (fun p -> p.x) in
  let max_y = get_max grid (fun p -> p.y) in
  let valid_xs =
    List.filter
      (can_fold grid max_y (fun a b -> { x = a; y = b }) target)
      (get_range max_x false)
  in
  let valid_ys =
    List.filter
      (can_fold grid max_x (fun a b -> { x = b; y = a }) target)
      (get_range max_y false)
  in
  sum valid_xs 1 + sum valid_ys 100

let () =
  let groups = Aoc.Reader.read_groups () in
  let grids = List.map Aoc.Grid.parse_grid groups in
  let part1 = List.fold_left ( + ) 0 (List.map (reflections 0) grids) in
  let part2 = List.fold_left ( + ) 0 (List.map (reflections 1) grids) in
  Aoc.Answer.part1 30487 part1 string_of_int;
  Aoc.Answer.part2 31954 part2 string_of_int
