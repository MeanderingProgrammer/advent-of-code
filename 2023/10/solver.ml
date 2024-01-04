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
  List.map
    ~f:(fun direction -> Point.move location direction 1)
    valid_directions

let rec traverse (grid : Grid.t) (locations : Point.t list)
    (seen : Types.PointSet.t) : Types.PointSet.t =
  let seen = Set.union seen (Types.PointSet.of_list locations) in
  let next_locations =
    List.concat (List.map ~f:(valid_adjacent grid) locations)
  in
  let next_locations =
    List.filter ~f:(fun location -> not (Set.mem seen location)) next_locations
  in
  if List.is_empty next_locations then seen
  else traverse grid next_locations seen

let increment (curr_char : char option) (prev_char : char) : bool =
  match curr_char with
  | None -> false
  | Some v -> (
      match v with
      | '|' -> true
      | 'J' -> Char.equal 'F' prev_char
      | '7' -> Char.equal 'L' prev_char
      | _ -> false)

let rec add_row (wall_counts : (Point.t, int) Hashtbl.t) (loop : Grid.t)
    (y : int) (prev_value : int) (prev_char : char) (x : int) (max_x : int) :
    unit =
  match x > max_x with
  | true -> ()
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
      Hashtbl.set wall_counts ~key:point ~data:curr_value;
      add_row wall_counts loop y curr_value next_char (x + 1) max_x

let rec add_wall_counts (wall_counts : (Point.t, int) Hashtbl.t) (loop : Grid.t)
    (max_x : int) (y : int) : unit =
  match y < 0 with
  | true -> ()
  | false ->
      add_row wall_counts loop y 0 '|' 0 max_x;
      add_wall_counts wall_counts loop max_x (y - 1)

let point_contained (wall_counts : (Point.t, int) Hashtbl.t) (point : Point.t) :
    bool =
  match Hashtbl.find wall_counts point with
  | None -> false
  | Some walls_after -> Int.equal (walls_after mod 2) 1

let contained (grid : Grid.t) (points : Types.PointSet.t) : int =
  let loop = Hashtbl.filter_keys ~f:(fun p -> Set.mem points p) grid in
  let max = Point.max (Set.to_list points) in
  let wall_counts = Hashtbl.create (module Point) in
  add_wall_counts wall_counts loop max.x max.y;
  let possible =
    List.filter ~f:(fun p -> not (Set.mem points p)) (Hashtbl.keys grid)
  in
  List.count ~f:(point_contained wall_counts) possible

let solution () =
  let grid = Reader.read_grid () in
  let start = Grid.find_value grid 'S' in
  Hashtbl.set grid ~key:start ~data:'F';
  let points = traverse grid [ start ] Types.PointSet.empty in
  let part1 = Set.length points / 2 in
  let part2 = contained grid points in
  Answer.part1 6690 part1 string_of_int;
  Answer.part2 525 part2 string_of_int

let () = Answer.timer solution
