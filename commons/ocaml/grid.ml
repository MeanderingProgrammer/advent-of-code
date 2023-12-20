open Core

type t = (Point.t * char) list

let grid_point (y : int) (x : int) (ch : char) : Point.t * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : t =
  let chars = String.to_list s in
  List.mapi ~f:(grid_point y) chars

let parse_grid (lines : string list) : t =
  List.concat (List.mapi ~f:grid_line lines)
