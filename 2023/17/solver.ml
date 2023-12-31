open Aoc
open Core

module Node = struct
  type t = { p : Point.t; ds : Direction.t list }
  [@@deriving compare, equal, hash, sexp]
end

module Edge = struct
  type 'a t = { n : 'a; w : int }

  let compare (e1 : 'a t) (e2 : 'a t) = Int.compare e1.w e2.w
end

let adjacent_line (p : Point.t) (length : int) (d : Direction.t option) :
    (Direction.t * Point.t list) list =
  (* Handle turning directions which must extend out to the specified length *)
  (* Initially all directions are considered a turn, afterwards it is the *)
  (* directions which are not straight or backwards *)
  let turns : Direction.t list =
    match d with
    | None -> [ UP; DOWN; LEFT; RIGHT ]
    | Some d -> Direction.get_turns d
  in
  let amounts = List.init length ~f:(fun i -> i + 1) in
  let result =
    List.map ~f:(fun d -> (d, List.map ~f:(Point.move p d) amounts)) turns
  in
  (* Add in the forward direction which does not need to exend to the length *)
  match d with None -> result | Some d -> (d, [ Point.move p d 1 ]) :: result

let neighbors (grid : Grid.t) (n : Node.t) (turn_resistance : int) :
    (Direction.t * Point.t list) list =
  let result = adjacent_line n.p turn_resistance (List.hd n.ds) in
  List.filter ~f:(fun (_, ps) -> Hashtbl.mem grid (List.last_exn ps)) result

(* Based on: https://github.com/jamespwilliams/aoc2021/blob/master/15/ocaml/common.ml *)
let dijkstra (grid : Grid.t) (start : Point.t) (target : Point.t)
    (turn_resistance : int) (allowed_repeats : int) : int =
  let get_heat (ps : Point.t list) : int =
    let heat_value p = Char.get_digit_exn (Hashtbl.find_exn grid p) in
    Util.sum (List.map ~f:heat_value ps)
  in

  let start_node : Node.t = { p = start; ds = [] } in

  let q = Pairing_heap.create ~cmp:Edge.compare () in
  Pairing_heap.add q { n = start_node; w = 0 };

  let distances = Hashtbl.create (module Node) in
  Hashtbl.add_exn distances ~key:start_node ~data:0;
  let get_distance (n : Node.t) : int =
    Hashtbl.find distances n |> Option.value ~default:Int.max_value
  in

  let rec run () : int =
    let e = Pairing_heap.pop_exn q in
    match Point.equal e.n.p target with
    | true -> e.w
    | false ->
        List.iter
          ~f:(fun ((d, ps) : Direction.t * Point.t list) ->
            let ds = List.init (List.length ps) ~f:(fun _ -> d) in
            let next_ds = List.take (ds @ e.n.ds) (allowed_repeats + 1) in
            let next_node : Node.t = { p = List.last_exn ps; ds = next_ds } in
            let distance = e.w + get_heat ps in
            let repeats = List.count ~f:(Direction.equal d) next_ds in
            if distance < get_distance next_node && repeats <= allowed_repeats
            then (
              Pairing_heap.add q { n = next_node; w = distance };
              Hashtbl.set distances ~key:next_node ~data:distance))
          (neighbors grid e.n turn_resistance);
        run ()
  in
  run ()

let () =
  let grid = Reader.read_grid () in
  let path_finder = dijkstra grid { x = 0; y = 0 } (Grid.max grid) in
  let part1 = path_finder 1 3 in
  let part2 = path_finder 4 10 in
  Answer.part1 694 part1 string_of_int;
  Answer.part2 829 part2 string_of_int
