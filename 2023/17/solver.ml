open Aoc
open Core

module Node = struct
  type t = { position : Point.t; directions : Direction.t list }
  [@@deriving compare, equal, hash, sexp]
end

module Edge = struct
  type t = { node : Node.t; weight : int }

  let compare (e1 : t) (e2 : t) = Int.compare e1.weight e2.weight
end

let adjacent_line (p : Point.t) (length : int) (d : Direction.t option) :
    (Direction.t * bool * Point.t list) list =
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
    List.map ~f:(fun d -> (d, true, List.map ~f:(Point.move p d) amounts)) turns
  in
  (* Add in the forward direction which does not need to extend to the length *)
  match d with
  | None -> result
  | Some d -> (d, false, [ Point.move p d 1 ]) :: result

let neighbors (grid : Grid.t) (n : Node.t) (turn_resistance : int) :
    (Direction.t * bool * Point.t list) list =
  let result =
    adjacent_line n.position turn_resistance (List.hd n.directions)
  in
  List.filter ~f:(fun (_, _, ps) -> Hashtbl.mem grid (List.last_exn ps)) result

(* Based on: https://github.com/jamespwilliams/aoc2021/blob/master/15/ocaml/common.ml *)
let dijkstra (grid : Grid.t) (start : Point.t) (target : Point.t)
    (turn_resistance : int) (allowed_repeats : int) : int =
  let get_heat (ps : Point.t list) : int =
    let heat_value p = Char.get_digit_exn (Hashtbl.find_exn grid p) in
    Util.sum (List.map ~f:heat_value ps)
  in

  let start_node : Node.t = { position = start; directions = [] } in

  let q = Pairing_heap.create ~cmp:Edge.compare () in
  Pairing_heap.add q { node = start_node; weight = 0 };

  let distances = Hashtbl.create (module Node) in
  Hashtbl.add_exn distances ~key:start_node ~data:0;
  let get_distance (n : Node.t) : int =
    Hashtbl.find distances n |> Option.value ~default:Int.max_value
  in

  let rec run () : int =
    let e = Pairing_heap.pop_exn q in
    match Point.equal e.node.position target with
    | true -> e.weight
    | false ->
        List.iter
          ~f:(fun ((d, is_turn, ps) : Direction.t * bool * Point.t list) ->
            let directions = List.init (List.length ps) ~f:(const d) in
            let next_directions =
              if is_turn then directions else directions @ e.node.directions
            in
            let next_node : Node.t =
              { position = List.last_exn ps; directions = next_directions }
            in
            let distance = e.weight + get_heat ps in
            let repeats = List.length next_node.directions in
            if distance < get_distance next_node && repeats <= allowed_repeats
            then (
              Pairing_heap.add q { node = next_node; weight = distance };
              Hashtbl.set distances ~key:next_node ~data:distance))
          (neighbors grid e.node turn_resistance);
        run ()
  in
  run ()

let solution () =
  let grid = Reader.read_grid () in
  let path_finder = dijkstra grid { x = 0; y = 0 } (Grid.max grid) in
  let part1 = path_finder 1 3 in
  let part2 = path_finder 4 10 in
  Answer.part1 694 part1 string_of_int;
  Answer.part2 829 part2 string_of_int

let () = Answer.timer solution
