open Core
open Direction

type point = { x : int; y : int }

let adjacent (p : point) : (direction * point) list =
  [
    (UP, { x = p.x; y = p.y - 1 });
    (DOWN, { x = p.x; y = p.y + 1 });
    (LEFT, { x = p.x - 1; y = p.y });
    (RIGHT, { x = p.x + 1; y = p.y });
  ]

let distance (p1 : point) (p2 : point) : int =
  Int.abs (p1.x - p2.x) + Int.abs (p1.y - p2.y)

let equal (p1 : point) (p2 : point) : bool =
  Int.equal p1.x p2.x && Int.equal p1.y p2.y
