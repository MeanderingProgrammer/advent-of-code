open Core
open Point

let grid_point (y : int) (x : int) (ch : char) : point * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (point * char) list =
  let chars = String.to_list s in
  List.mapi ~f:(grid_point y) chars

let parse_grid (lines : string list) : (point * char) list =
  Stdlib.List.flatten (List.mapi ~f:grid_line lines)
