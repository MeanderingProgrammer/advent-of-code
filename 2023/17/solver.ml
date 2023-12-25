open Core
open Printf

module Node = struct
  type t = Aoc.Point.t * Aoc.Direction.t list
  [@@deriving compare, equal, hash, sexp]
end

module Edge = struct
  type 'a t = 'a * int

  let compare ((_, w1) : 'a t) ((_, w2) : 'a t) = Int.compare w1 w2
end

let neighbor_string ((d, p) : Aoc.Direction.t * Aoc.Point.t) : string =
  sprintf "[%s %s]" (Aoc.Point.to_string p) (Aoc.Direction.to_string d)

let neighbors (grid : Aoc.Grid.t) (p : Aoc.Point.t) :
    (Aoc.Direction.t * Aoc.Point.t) list =
  let result = Aoc.Point.adjacent p in
  List.filter ~f:(fun (_, p) -> Hashtbl.mem grid p) result

let dijkstra (grid : Aoc.Grid.t) (start : Aoc.Point.t) =
  let q = Pairing_heap.create ~cmp:Edge.compare () in
  Pairing_heap.add q (start, 0);

  let distances = Hashtbl.create (module Node) in
  (* Hashtbl.add_exn distances ~key:start ~data:0; *)
  printf "EMPTY %b\n" (Hashtbl.is_empty distances);

  while not (Pairing_heap.is_empty q) do
    let p, w = Pairing_heap.pop_exn q in
    printf "%s -> %d\n" (Aoc.Point.to_string p) w;
    let adjacent = neighbors grid p in
    printf "NEIGHBORS = %s\n" (List.to_string ~f:neighbor_string adjacent)
  done

let () =
  let grid = Aoc.Reader.read_grid () in
  let start : Aoc.Point.t = { x = 0; y = 0 } in
  let target : Aoc.Point.t = Aoc.Grid.max grid in
  dijkstra grid start;
  printf "END = %s\n" (Aoc.Point.to_string target);
  Aoc.Answer.part1 1 1 string_of_int
