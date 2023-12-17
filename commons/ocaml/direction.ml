type direction = UP | DOWN | LEFT | RIGHT

let to_string (d : direction) : string =
  match d with UP -> "UP" | DOWN -> "DOWN" | LEFT -> "LEFT" | RIGHT -> "RIGHT"

let equal (d1 : direction) (d2 : direction) : bool =
  String.equal (to_string d1) (to_string d2)
