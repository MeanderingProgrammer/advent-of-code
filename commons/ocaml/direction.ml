type t = UP | DOWN | LEFT | RIGHT [@@deriving compare, equal, hash, sexp]

let to_string (d : t) : string =
  match d with UP -> "UP" | DOWN -> "DOWN" | LEFT -> "LEFT" | RIGHT -> "RIGHT"

let get_turns (d : t) : t list =
  match d with UP | DOWN -> [ LEFT; RIGHT ] | LEFT | RIGHT -> [ UP; DOWN ]
