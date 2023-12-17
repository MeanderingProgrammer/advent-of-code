open Core

let grid_point (y : int) (x : int) (ch : char) : Point.t * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (Point.t * char) list =
  let chars = String.to_list s in
  List.mapi ~f:(grid_point y) chars

let parse_grid (lines : string list) : (Point.t * char) list =
  List.concat (List.mapi ~f:grid_line lines)