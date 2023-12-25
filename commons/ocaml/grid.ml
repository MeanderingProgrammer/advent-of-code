open Core

type t = (Point.t, char) Hashtbl.t

let grid_point (y : int) (x : int) (ch : char) : Point.t * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (Point.t * char) list =
  let chars = String.to_list s in
  List.mapi ~f:(grid_point y) chars

let parse_grid (lines : string list) : t =
  let grid = List.concat (List.mapi ~f:grid_line lines) in
  Hashtbl.of_alist_exn (module Point) grid

let max (grid : t) : Point.t = Point.max (Hashtbl.keys grid)

let to_string (grid : t) : string =
  let max_point = max grid in
  let xs = List.init (max_point.x + 1) ~f:Util.identity in
  let ys = List.init (max_point.y + 1) ~f:Util.identity in
  let row (y : int) : string =
    let values = List.map ~f:(fun x -> Hashtbl.find_exn grid { x; y }) xs in
    String.of_char_list values
  in
  String.concat ~sep:"\n" (List.map ~f:row ys)
