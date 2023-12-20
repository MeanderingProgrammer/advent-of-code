open Core

let valid_adjacent grid location =
  let pipe = List.Assoc.find_exn ~equal:Aoc.Point.equal grid location in
  let valid_directions =
    match pipe with
    | '|' -> [ Aoc.Direction.UP; DOWN ]
    | '-' -> [ LEFT; RIGHT ]
    | 'L' -> [ UP; RIGHT ]
    | 'J' -> [ UP; LEFT ]
    | '7' -> [ DOWN; LEFT ]
    | 'F' -> [ DOWN; RIGHT ]
    | _ -> raise (Invalid_argument (Char.to_string pipe))
  in
  let locations = Aoc.Point.adjacent location in
  let valid_locations =
    List.filter
      ~f:(fun (direction, _) ->
        List.exists ~f:(Aoc.Direction.equal direction) valid_directions)
      locations
  in
  List.map ~f:(fun (_, location) -> location) valid_locations

let rec traverse grid steps locations seen =
  let seen = List.map ~f:(fun location -> (location, steps)) locations @ seen in
  let next_locations =
    List.concat (List.map ~f:(valid_adjacent grid) locations)
  in
  let next_locations =
    List.filter
      ~f:(fun location ->
        Option.is_none (List.Assoc.find ~equal:Aoc.Point.equal seen location))
      next_locations
  in
  if List.is_empty next_locations then seen
  else traverse grid (steps + 1) next_locations seen

let increment (curr_char : char option) (prev_char : char) : bool =
  match curr_char with
  | None -> false
  | Some v -> (
      match v with
      | '|' -> true
      | 'J' -> Char.equal 'F' prev_char
      | '7' -> Char.equal 'L' prev_char
      | _ -> false)

let rec row_wall_counts (loop : Aoc.Grid.t) (y : int) (prev_value : int)
    (prev_char : char) (x : int) (max_x : int) : (Aoc.Point.t * int) list =
  match x > max_x with
  | true -> []
  | false ->
      let point : Aoc.Point.t = { x; y } in
      let curr_char = List.Assoc.find ~equal:Aoc.Point.equal loop point in
      let curr_value =
        prev_value + if increment curr_char prev_char then 1 else 0
      in
      let next_char =
        match curr_char with
        | None -> prev_char
        | Some v -> if Char.equal '-' v then prev_char else v
      in
      (point, curr_value)
      :: row_wall_counts loop y curr_value next_char (x + 1) max_x

let rec get_wall_counts (loop : Aoc.Grid.t) (max_x : int) (y : int) :
    (Aoc.Point.t * int) list =
  match y < 0 with
  | true -> []
  | false ->
      let row = row_wall_counts loop y 0 '|' 0 max_x in
      row @ get_wall_counts loop max_x (y - 1)

let point_contained (wall_counts : (Aoc.Point.t * int) list)
    (point : Aoc.Point.t) : bool =
  match List.Assoc.find ~equal:Aoc.Point.equal wall_counts point with
  | None -> false
  | Some walls_after -> Int.equal (walls_after mod 2) 1

let contained (grid : Aoc.Grid.t) (points : Aoc.Point.t list) : int =
  let possible, _ = List.unzip grid in
  let not_in p = not (List.mem ~equal:Aoc.Point.equal points p) in
  let possible = List.filter ~f:not_in possible in
  let grid_value p = List.Assoc.find_exn ~equal:Aoc.Point.equal grid p in
  let loop = List.map ~f:(fun p -> (p, grid_value p)) points in
  let max_x = Aoc.Util.max (List.map ~f:(fun p -> p.x) points) in
  let max_y = Aoc.Util.max (List.map ~f:(fun p -> p.y) points) in
  let wall_counts = get_wall_counts loop max_x max_y in
  List.count ~f:(point_contained wall_counts) possible

let () =
  let grid = Aoc.Reader.read_grid () in
  let start, _ = List.find_exn ~f:(fun (_, ch) -> Char.equal ch 'S') grid in
  let grid = List.Assoc.remove ~equal:Aoc.Point.equal grid start in
  let grid = (start, 'F') :: grid in
  let point_distances = traverse grid 0 [ start ] [] in
  let points, distances = List.unzip point_distances in
  let part1 = Aoc.Util.max distances in
  let part2 = contained grid points in
  Aoc.Answer.part1 6690 part1 string_of_int;
  Aoc.Answer.part2 525 part2 string_of_int
