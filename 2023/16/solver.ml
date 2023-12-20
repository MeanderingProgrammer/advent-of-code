open Core
(* open Printf *)

type state = { position : Aoc.Point.t; direction : Aoc.Direction.t }

let state_equal (s1 : state) (s2 : state) : bool =
  Aoc.Point.equal s1.position s2.position
  && Aoc.Direction.equal s1.direction s2.direction

(* let state_string (s : state) : string = *)
(*   sprintf "%s | %s" *)
(*     (Aoc.Point.to_string s.position) *)
(*     (Aoc.Direction.to_string s.direction) *)

let next_directions grid (s : state) : Aoc.Direction.t list =
  let value = List.Assoc.find_exn ~equal:Aoc.Point.equal grid s.position in
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

let next_states grid s =
  let directions = next_directions grid s in
  List.map ~f:(next_state s) directions

let grid_contains grid s = List.Assoc.mem ~equal:Aoc.Point.equal grid s.position
let unexplored explored s = not (List.mem ~equal:state_equal explored s)

let move_states grid explored states =
  let states = List.concat (List.map ~f:(next_states grid) states) in
  let states = List.filter ~f:(grid_contains grid) states in
  List.filter ~f:(unexplored explored) states

let rec follow grid explored current =
  let next = move_states grid explored current in
  if List.is_empty next then explored else follow grid (next @ explored) next

let rec get_energized explored =
  match explored with
  | [] -> []
  | x :: xs ->
      let position = x.position in
      let energized = get_energized xs in
      if List.mem ~equal:Aoc.Point.equal energized position then energized
      else position :: energized

let () =
  let grid = Aoc.Reader.read_grid () in
  let start =
    { position = { x = 0; y = 0 }; direction = Aoc.Direction.RIGHT }
  in
  let explored = follow grid [ start ] [ start ] in
  let energized = get_energized explored in
  (* printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:Aoc.Point.to_string energized)); *)
  let part1 = List.length energized in
  Aoc.Answer.part1 46 part1 string_of_int
