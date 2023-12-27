open Core

type t = (Point.t, char) Hashtbl.t

let grid_point (y : int) (x : int) (ch : char) : Point.t * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (Point.t * char) list =
  let chars = String.to_list s in
  List.mapi ~f:(grid_point y) chars

let parse_grid (lines : string list) : t =
  let grid = List.concat (List.mapi ~f:grid_line lines) in
  Hashtbl.of_alist_exn (module Point) grid

let min (grid : t) : Point.t = Point.min (Hashtbl.keys grid)
let max (grid : t) : Point.t = Point.max (Hashtbl.keys grid)

let find_value (grid : t) (value : char) : Point.t =
  let with_value = Hashtbl.filter ~f:(Char.equal value) grid in
  let points, _ = List.unzip (Hashtbl.to_alist with_value) in
  assert (Int.equal 1 (List.length points));
  List.hd_exn points

let get (grid : t) (p : Point.t) : char =
  match Hashtbl.find grid p with None -> '.' | Some ch -> ch

let to_string (grid : t) : string =
  let min_p = min grid in
  let max_p = max grid in
  let xs = List.init (max_p.x - min_p.x + 1) ~f:(fun x -> x + min_p.x) in
  let ys = List.init (max_p.y - min_p.y + 1) ~f:(fun y -> y + min_p.y) in
  let row (y : int) : string =
    let values = List.map ~f:(fun x -> get grid { x; y }) xs in
    String.of_char_list values
  in
  String.concat ~sep:"\n" (List.map ~f:row ys)
