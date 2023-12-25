open Core

type universe_data = { x_expansions : int list; y_expansions : int list }

let rec get_holes (grid_values : int list) (value : int) : int list =
  match value < 0 with
  | true -> []
  | false ->
      let hole =
        if List.mem ~equal:Int.equal grid_values value then [] else [ value ]
      in
      hole @ get_holes grid_values (value - 1)

let rec points_between (expansions : int list) (v1 : int) (v2 : int) : int =
  match expansions with
  | [] -> 0
  | x :: xs ->
      let result = if x >= Int.min v1 v2 && x <= Int.max v1 v2 then 1 else 0 in
      result + points_between xs v1 v2

let get_distance universe x y multiplier =
  let initial_distance = Aoc.Point.distance x y in
  let x_between = points_between universe.x_expansions x.x y.x in
  let y_between = points_between universe.y_expansions x.y y.y in
  initial_distance + ((x_between + y_between) * (multiplier - 1))

let rec get_distance_pairs universe x points multiplier =
  match points with
  | [] -> []
  | y :: ys ->
      get_distance universe x y multiplier
      :: get_distance_pairs universe x ys multiplier

let rec get_distances universe points multiplier =
  match points with
  | [] -> []
  | x :: xs ->
      get_distance_pairs universe x xs multiplier
      @ get_distances universe xs multiplier

let sum_distances universe points multiplier =
  Aoc.Util.sum (get_distances universe points multiplier)

let () =
  let grid = Aoc.Reader.read_grid () in
  let grid = Hashtbl.filter ~f:(Char.equal '#') grid in
  let max = Aoc.Grid.max grid in
  let grid = Hashtbl.keys grid in
  let universe =
    {
      x_expansions = get_holes (List.map ~f:Aoc.Point.get_x grid) max.x;
      y_expansions = get_holes (List.map ~f:Aoc.Point.get_y grid) max.y;
    }
  in
  let part1 = sum_distances universe grid 2 in
  let part2 = sum_distances universe grid 1_000_000 in
  Aoc.Answer.part1 9550717 part1 string_of_int;
  Aoc.Answer.part2 648458253817 part2 string_of_int
