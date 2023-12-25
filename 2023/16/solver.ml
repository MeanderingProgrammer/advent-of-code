open Core
module PointSet = Set.Make (Aoc.Point)

type state = { position : Aoc.Point.t; direction : Aoc.Direction.t }

let state_equal (s1 : state) (s2 : state) : bool =
  Aoc.Point.equal s1.position s2.position
  && Aoc.Direction.equal s1.direction s2.direction

let next_directions (grid : Aoc.Grid.t) (s : state) : Aoc.Direction.t list =
  let value = Hashtbl.find_exn grid s.position in
  match value with
  | '.' -> [ s.direction ]
  | '|' -> (
      match s.direction with
      | UP -> [ s.direction ]
      | DOWN -> [ s.direction ]
      | LEFT -> [ UP; DOWN ]
      | RIGHT -> [ UP; DOWN ])
  | '-' -> (
      match s.direction with
      | UP -> [ LEFT; RIGHT ]
      | DOWN -> [ LEFT; RIGHT ]
      | LEFT -> [ s.direction ]
      | RIGHT -> [ s.direction ])
  | '\\' -> (
      match s.direction with
      | UP -> [ LEFT ]
      | DOWN -> [ RIGHT ]
      | LEFT -> [ UP ]
      | RIGHT -> [ DOWN ])
  | '/' -> (
      match s.direction with
      | UP -> [ RIGHT ]
      | DOWN -> [ LEFT ]
      | LEFT -> [ DOWN ]
      | RIGHT -> [ UP ])
  | _ -> raise (Invalid_argument (Char.to_string value))

let move (position : Aoc.Point.t) (direction : Aoc.Direction.t) : Aoc.Point.t =
  match direction with
  | UP -> { position with y = position.y - 1 }
  | DOWN -> { position with y = position.y + 1 }
  | LEFT -> { position with x = position.x - 1 }
  | RIGHT -> { position with x = position.x + 1 }

let next_state (s : state) (direction : Aoc.Direction.t) : state =
  { position = move s.position direction; direction }

let next_states (grid : Aoc.Grid.t) (s : state) : state list =
  let directions = next_directions grid s in
  List.map ~f:(next_state s) directions

let grid_contains (grid : Aoc.Grid.t) (s : state) : bool =
  Hashtbl.mem grid s.position

let unexplored (explored : state list) (s : state) : bool =
  not (List.mem ~equal:state_equal explored s)

let move_states (grid : Aoc.Grid.t) (explored : state list)
    (states : state list) : state list =
  let states = List.concat (List.map ~f:(next_states grid) states) in
  let states = List.filter ~f:(grid_contains grid) states in
  List.filter ~f:(unexplored explored) states

let rec follow (grid : Aoc.Grid.t) (explored : state list)
    (current : state list) =
  let next = move_states grid explored current in
  if List.is_empty next then explored else follow grid (next @ explored) next

let get_energized (grid : Aoc.Grid.t) (start : state) : int =
  let explored = follow grid [ start ] [ start ] in
  Set.length (PointSet.of_list (List.map ~f:(fun s -> s.position) explored))

let rec max_energized (grid : Aoc.Grid.t) (points : Aoc.Point.t list) : int =
  match points with
  | [] -> 0
  | position :: xs ->
      let energized =
        Aoc.Util.max
          [
            get_energized grid { position; direction = UP };
            get_energized grid { position; direction = DOWN };
            get_energized grid { position; direction = LEFT };
            get_energized grid { position; direction = RIGHT };
          ]
      in
      Int.max energized (max_energized grid xs)

let () =
  let grid = Aoc.Reader.read_grid () in
  let start =
    { position = { x = 0; y = 0 }; direction = Aoc.Direction.RIGHT }
  in
  let part1 = get_energized grid start in
  let side = (Aoc.Grid.max grid).x in
  let coords = List.init (side + 1) ~f:Aoc.Util.identity in
  let points =
    List.map ~f:(fun (x : int) : Aoc.Point.t -> { x; y = 0 }) coords
  in
  let points =
    points @ List.map ~f:(fun (x : int) : Aoc.Point.t -> { x; y = side }) coords
  in
  let points =
    points @ List.map ~f:(fun (y : int) : Aoc.Point.t -> { x = 0; y }) coords
  in
  let points =
    points @ List.map ~f:(fun (y : int) : Aoc.Point.t -> { x = side; y }) coords
  in
  let part2 = max_energized grid points in
  Aoc.Answer.part1 8901 part1 string_of_int;
  Aoc.Answer.part2 9064 part2 string_of_int
