type t = UP | DOWN | LEFT | RIGHT [@@deriving equal]

let to_string (d : t) : string =
  match d with UP -> "UP" | DOWN -> "DOWN" | LEFT -> "LEFT" | RIGHT -> "RIGHT"
