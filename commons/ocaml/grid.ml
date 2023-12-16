open Point

let grid_point (y : int) (x : int) (ch : char) : point * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (point * char) list =
  let chars = s |> String.to_seq |> List.of_seq in
  List.mapi (grid_point y) chars

let parse_grid (lines : string list) : (point * char) list =
  List.flatten (List.mapi grid_line lines)
