open Core

type state = { position : Aoc.Point.t; direction : Aoc.Direction.t }

let state_equal (s1 : state) (s2 : state) : bool =
  Aoc.Point.equal s1.position s2.position
  && Aoc.Direction.equal s1.direction s2.direction

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

let next_states (grid : Aoc.Grid.t) s =
  let directions = next_directions grid s in
  List.map ~f:(next_state s) directions

let grid_contains (grid : Aoc.Grid.t) s =
  List.Assoc.mem ~equal:Aoc.Point.equal grid s.position

let unexplored explored s = not (List.mem ~equal:state_equal explored s)

let move_states (grid : Aoc.Grid.t) (explored : state list)
    (states : state list) =
  let states = List.concat (List.map ~f:(next_states grid) states) in
  let states = List.filter ~f:(grid_contains grid) states in
  List.filter ~f:(unexplored explored) states

let rec follow (grid : Aoc.Grid.t) (explored : state list)
    (current : state list) =
  let next = move_states grid explored current in
  if List.is_empty next then explored else follow grid (next @ explored) next

let get_explored (grid : Aoc.Grid.t) (start : state) : state list =
  follow grid [ start ] [ start ]

let rec get_energized (explored : state list) : Aoc.Point.t list =
  match explored with
  | [] -> []
  | x :: xs ->
      let position = x.position in
      let energized = get_energized xs in
      if List.mem ~equal:Aoc.Point.equal energized position then energized
      else position :: energized

let () =
  (* For part 2 we can probably ignore positions that were explored as part of *)
  (* other starting points *)
  let grid = Aoc.Reader.read_grid () in
  let start =
    { position = { x = 0; y = 0 }; direction = Aoc.Direction.RIGHT }
  in
  let explored = get_explored grid start in
  let energized = get_energized explored in
  let part1 = List.length energized in
  (* Aoc.Answer.part1 8901 part1 string_of_int; *)
  Aoc.Answer.part1 46 part1 string_of_int
