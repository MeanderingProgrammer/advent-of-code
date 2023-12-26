open Core

type t = { x : int; y : int } [@@deriving compare, equal, hash, sexp]

let get_x (p : t) : int = p.x
let get_y (p : t) : int = p.y
let to_string (p : t) : string = Printf.sprintf "(%d, %d)" p.x p.y

let move (p : t) (d : Direction.t) (amount : int) : t =
  match d with
  | UP -> { p with y = p.y - amount }
  | DOWN -> { p with y = p.y + amount }
  | LEFT -> { p with x = p.x - amount }
  | RIGHT -> { p with x = p.x + amount }

let adjacent (p : t) : (Direction.t * t) list =
  [
    (UP, move p UP 1);
    (DOWN, move p DOWN 1);
    (LEFT, move p LEFT 1);
    (RIGHT, move p RIGHT 1);
  ]

let distance (p1 : t) (p2 : t) : int =
  Int.abs (p1.x - p2.x) + Int.abs (p1.y - p2.y)

let max (points : t list) : t =
  let max_of (f : t -> int) : int = Util.max (List.map ~f points) in
  { x = max_of get_x; y = max_of get_y }
