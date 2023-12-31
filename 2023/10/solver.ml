open Aoc
open Core

let valid_adjacent (grid : Grid.t) (location : Point.t) =
  let pipe = Hashtbl.find_exn grid location in
  let valid_directions =
    match pipe with
    | '|' -> [ Direction.UP; DOWN ]
    | '-' -> [ LEFT; RIGHT ]
    | 'L' -> [ UP; RIGHT ]
    | 'J' -> [ UP; LEFT ]
    | '7' -> [ DOWN; LEFT ]
    | 'F' -> [ DOWN; RIGHT ]
    | _ -> raise (Invalid_argument (Char.to_string pipe))
  in
  let locations = Point.adjacent location in
  let valid_locations =
    List.filter
      ~f:(fun (direction, _) ->
        List.exists ~f:(Direction.equal direction) valid_directions)
      locations
  in
  List.map ~f:(fun (_, location) -> location) valid_locations

let rec traverse (grid : Grid.t) steps locations seen =
  let seen = List.map ~f:(fun location -> (location, steps)) locations @ seen in
  let next_locations =
    List.concat (List.map ~f:(valid_adjacent grid) locations)
  in
  let next_locations =
    List.filter
      ~f:(fun location ->
        Option.is_none (List.Assoc.find ~equal:Point.equal seen location))
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

let rec row_wall_counts (loop : Grid.t) (y : int) (prev_value : int)
    (prev_char : char) (x : int) (max_x : int) : (Point.t * int) list =
  match x > max_x with
  | true -> []
  | false ->
      let point : Point.t = { x; y } in
      let curr_char = Hashtbl.find loop point in
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

let rec get_wall_counts (loop : Grid.t) (max_x : int) (y : int) :
    (Point.t * int) list =
  match y < 0 with
  | true -> []
  | false ->
      let row = row_wall_counts loop y 0 '|' 0 max_x in
      row @ get_wall_counts loop max_x (y - 1)

let point_contained (wall_counts : (Point.t * int) list) (point : Point.t) :
    bool =
  match List.Assoc.find ~equal:Point.equal wall_counts point with
  | None -> false
  | Some walls_after -> Int.equal (walls_after mod 2) 1

let contained (grid : Grid.t) (points : Point.t list) : int =
  let possible = Hashtbl.keys grid in
  let not_in p = not (List.mem ~equal:Point.equal points p) in
  let possible = List.filter ~f:not_in possible in
  let loop =
    Hashtbl.filter_keys ~f:(fun p -> List.mem ~equal:Point.equal points p) grid
  in
  let max = Point.max points in
  let wall_counts = get_wall_counts loop max.x max.y in
  List.count ~f:(point_contained wall_counts) possible

let () =
  let grid = Reader.read_grid () in
  let start = Grid.find_value grid 'S' in
  Hashtbl.set grid ~key:start ~data:'F';
  let point_distances = traverse grid 0 [ start ] [] in
  let points, distances = List.unzip point_distances in
  let part1 = Util.max distances in
  let part2 = contained grid points in
  Answer.part1 6690 part1 string_of_int;
  Answer.part2 525 part2 string_of_int
