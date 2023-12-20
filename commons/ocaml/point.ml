open Core

type t = { x : int; y : int }

let compare = Stdlib.compare
let equal (p1 : t) (p2 : t) : bool = Int.equal p1.x p2.x && Int.equal p1.y p2.y
let hash (p : t) : int = Hashtbl.hash (p.x, p.y)
let to_string (p : t) : string = Printf.sprintf "(%d, %d)" p.x p.y

let sexp_of_t (p : t) =
  Sexp.List
    [ Sexp.Atom "x"; Int.sexp_of_t p.x; Sexp.Atom "y"; Int.sexp_of_t p.y ]

let adjacent (p : t) : (Direction.t * t) list =
  [
    (UP, { x = p.x; y = p.y - 1 });
    (DOWN, { x = p.x; y = p.y + 1 });
    (LEFT, { x = p.x - 1; y = p.y });
    (RIGHT, { x = p.x + 1; y = p.y });
  ]

let distance (p1 : t) (p2 : t) : int =
  Int.abs (p1.x - p2.x) + Int.abs (p1.y - p2.y)
