open Core

type direction = UP | DOWN | LEFT | RIGHT

let direction_string (d : direction) : string =
  match d with UP -> "UP" | DOWN -> "DOWN" | LEFT -> "LEFT" | RIGHT -> "RIGHT"

let direction_equal (d1 : direction) (d2 : direction) : bool =
  String.equal (direction_string d1) (direction_string d2)

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

let point_equal (p1 : point) (p2 : point) : bool =
  Int.equal p1.x p2.x && Int.equal p1.y p2.y
