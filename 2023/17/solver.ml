open Core
open Printf

let neighbor_string ((d, p) : Aoc.Direction.t * Aoc.Point.t) : string =
  sprintf "[%s %s]" (Aoc.Point.to_string p) (Aoc.Direction.to_string d)

let neighbors (grid : Aoc.Grid.t) (p : Aoc.Point.t) :
    (Aoc.Direction.t * Aoc.Point.t) list =
  let result = Aoc.Point.adjacent p in
  List.filter ~f:(fun (_, p) -> Hashtbl.mem grid p) result

let () =
  let grid = Aoc.Reader.read_grid () in
  let start : Aoc.Point.t = { x = 0; y = 0 } in
  let target : Aoc.Point.t =
    {
      x = Aoc.Util.max (List.map ~f:(fun p -> p.x) (Hashtbl.keys grid));
      y = Aoc.Util.max (List.map ~f:(fun p -> p.y) (Hashtbl.keys grid));
    }
  in
  printf "START = %s\n" (Aoc.Point.to_string start);
  printf "NEIGHBORS = %s\n"
    (List.to_string ~f:neighbor_string (neighbors grid start));
  printf "END = %s\n" (Aoc.Point.to_string target);
  Aoc.Answer.part1 1 1 string_of_int
