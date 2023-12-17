type t = UP | DOWN | LEFT | RIGHT

let to_string (d : t) : string =
  match d with UP -> "UP" | DOWN -> "DOWN" | LEFT -> "LEFT" | RIGHT -> "RIGHT"

let equal (d1 : t) (d2 : t) : bool = String.equal (to_string d1) (to_string d2)
