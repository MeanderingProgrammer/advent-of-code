open Core
open Aoc.Point

type universe_data = { x_expansions : int list; y_expansions : int list }

let rec get_holes grid f current max =
  if Int.equal current max then []
  else if List.exists ~f:(fun p -> Int.equal (f p) current) grid then
    get_holes grid f (current + 1) max
  else current :: get_holes grid f (current + 1) max

let get_universe grid =
  let xs = List.map ~f:(fun p -> p.x) grid in
  let ys = List.map ~f:(fun p -> p.y) grid in
  let max_x =
    List.fold_left ~init:(List.hd_exn xs) ~f:Int.max (List.tl_exn xs)
  in
  let max_y =
    List.fold_left ~init:(List.hd_exn ys) ~f:Int.max (List.tl_exn ys)
  in
  {
    x_expansions = get_holes grid (fun p -> p.x) 0 max_x;
    y_expansions = get_holes grid (fun p -> p.y) 0 max_y;
  }

let rec points_between expansions v1 v2 =
  match expansions with
  | x :: xs ->
      let result = if x >= Int.min v1 v2 && x <= Int.max v1 v2 then 1 else 0 in
      result + points_between xs v1 v2
  | [] -> 0

let get_distance universe x y multiplier =
  let initial_distance = distance x y in
  let x_between = points_between universe.x_expansions x.x y.x in
  let y_between = points_between universe.y_expansions x.y y.y in
  initial_distance + ((x_between + y_between) * (multiplier - 1))

let rec get_distance_pairs universe x points multiplier =
  match points with
  | y :: ys ->
      get_distance universe x y multiplier
      :: get_distance_pairs universe x ys multiplier
  | [] -> []

let rec get_distances universe points multiplier =
  match points with
  | x :: xs ->
      get_distance_pairs universe x xs multiplier
      @ get_distances universe xs multiplier
  | [] -> []

let sum_distances universe points multiplier =
  let distances = get_distances universe points multiplier in
  List.fold_left ~init:0 ~f:( + ) distances

let () =
  let grid = Aoc.Reader.read_grid () in
  let grid = List.filter ~f:(fun (_, ch) -> Char.equal ch '#') grid in
  let grid = List.map ~f:(fun (p, _) -> p) grid in
  let universe = get_universe grid in
  let part1 = sum_distances universe grid 2 in
  let part2 = sum_distances universe grid 1_000_000 in
  Aoc.Answer.part1 9550717 part1 string_of_int;
  Aoc.Answer.part2 648458253817 part2 string_of_int
