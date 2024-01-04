open Aoc
open Core

module State = struct
  type t = { position : Point.t; direction : Direction.t }
  [@@deriving compare, sexp]
end

module StateSet = Set.Make (State)

let next_directions (grid : Grid.t) (s : State.t) : Direction.t list =
  let value = Hashtbl.find_exn grid s.position in
  match value with
  | '.' -> [ s.direction ]
  | '|' -> (
      match s.direction with
      | UP | DOWN -> [ s.direction ]
      | LEFT | RIGHT -> [ UP; DOWN ])
  | '-' -> (
      match s.direction with
      | UP | DOWN -> [ LEFT; RIGHT ]
      | LEFT | RIGHT -> [ s.direction ])
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

let move (position : Point.t) (direction : Direction.t) : Point.t =
  match direction with
  | UP -> { position with y = position.y - 1 }
  | DOWN -> { position with y = position.y + 1 }
  | LEFT -> { position with x = position.x - 1 }
  | RIGHT -> { position with x = position.x + 1 }

let next_state (s : State.t) (direction : Direction.t) : State.t =
  { position = move s.position direction; direction }

let next_states (grid : Grid.t) (s : State.t) : State.t list =
  let grid_contains (s : State.t) : bool = Hashtbl.mem grid s.position in
  let directions = next_directions grid s in
  let states = List.map ~f:(next_state s) directions in
  List.filter ~f:grid_contains states

let move_states (grid : Grid.t) (explored : StateSet.t) (states : State.t list)
    : State.t list =
  let unexplored (s : State.t) : bool = not (Set.mem explored s) in
  let states = List.concat (List.map ~f:(next_states grid) states) in
  List.filter ~f:unexplored states

let rec follow (grid : Grid.t) (explored : StateSet.t) (current : State.t list)
    =
  let next = move_states grid explored current in
  let explored = Set.union explored (StateSet.of_list next) in
  if List.is_empty next then explored else follow grid explored next

let energized (grid : Grid.t) (start : State.t) : int =
  let explored = follow grid (StateSet.of_list [ start ]) [ start ] in
  let points = List.map ~f:(fun s -> s.position) (Set.to_list explored) in
  Set.length (Types.PointSet.of_list points)

let create_states (coords : int list) (direction : Direction.t)
    (f : int -> Point.t) : State.t list =
  List.map
    ~f:(fun (coord : int) : State.t -> { position = f coord; direction })
    coords

let solution () =
  let grid = Reader.read_grid () in
  let start : State.t = { position = { x = 0; y = 0 }; direction = RIGHT } in
  let part1 = energized grid start in
  let side = (Grid.max grid).x in
  let coords = List.init (side + 1) ~f:Util.identity in
  let states : State.t list =
    create_states coords DOWN (fun x -> { x; y = 0 })
    @ create_states coords UP (fun x -> { x; y = side })
    @ create_states coords RIGHT (fun y -> { x = 0; y })
    @ create_states coords LEFT (fun y -> { x = side; y })
  in
  let part2 = Util.max (List.map ~f:(energized grid) states) in
  Answer.part1 8901 part1 string_of_int;
  Answer.part2 9064 part2 string_of_int

let () = Answer.timer solution
