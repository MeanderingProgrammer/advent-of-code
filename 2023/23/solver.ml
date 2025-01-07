open Aoc
open Core

type trace = { path : Point.t list; dir : Direction.t; uphill : bool }
type edge = { point : Point.t; dir : Direction.t; length : int; uphill : bool }
type graph = (Point.t, edge list) Hashtbl.t

let path_equal (t1 : trace) (t2 : trace) : bool =
  List.equal Point.equal t1.path t2.path

let valid_space (grid : Grid.t) (point : Point.t) : bool =
  match Hashtbl.find grid point with
  | None -> false
  | Some ch -> not (Char.equal '#' ch)

let unseen (trace : trace) (point : Point.t) : bool =
  not (List.mem ~equal:Point.equal trace.path point)

let goes_uphill (value : char) (dir : Direction.t) : bool =
  match value with
  | '^' -> not (Direction.equal UP dir)
  | 'v' -> not (Direction.equal DOWN dir)
  | '<' -> not (Direction.equal LEFT dir)
  | '>' -> not (Direction.equal RIGHT dir)
  | _ -> false

let neighbors (grid : Grid.t) (trace : trace) :
    (Point.t * Direction.t * bool) list =
  let current = List.hd_exn trace.path in
  (* Continue path in all directions from last point on our path *)
  let result = Point.adjacent current in
  (* Remove anything that's off the grid or goes into a forest *)
  let result =
    List.filter ~f:(fun (_, point) -> valid_space grid point) result
  in
  (* Remove direction going back the way we traveled *)
  let result = List.filter ~f:(fun (_, point) -> unseen trace point) result in
  (* Add information about whether the step went uphill *)
  let value = Hashtbl.find_exn grid current in
  List.map ~f:(fun (dir, point) -> (point, dir, goes_uphill value dir)) result

(* Lots of this grid is single option moves, this method collapses all *)
(* of this information into a dense representation *)
let rec collapse (graph : graph) (grid : Grid.t) (traces : trace list) : graph =
  match traces with
  | [] -> graph
  | x :: xs -> (
      let options = neighbors grid x in
      match List.length options with
      | 1 ->
          let point, _, uphill = List.hd_exn options in
          let trace =
            { path = point :: x.path; dir = x.dir; uphill = uphill || x.uphill }
          in
          collapse graph grid (trace :: xs)
      | _ ->
          let path = List.rev x.path in
          let src = List.hd_exn path in
          let dst = List.last_exn path in
          (* Add current edge to the graph *)
          let edge =
            {
              point = dst;
              dir = x.dir;
              length = List.length path - 1;
              uphill = x.uphill;
            }
          in
          let edges =
            match Hashtbl.find graph src with
            | None -> [ edge ]
            | Some es -> edge :: es
          in
          Hashtbl.set graph ~key:src ~data:edges;
          (* Check existing edges from the destination to avoid re-exploring options *)
          let explored =
            match Hashtbl.find graph dst with
            | None -> []
            | Some es -> List.map ~f:(fun e -> e.dir) es
          in
          let options =
            List.filter
              ~f:(fun (_, dir, _) ->
                not (List.mem ~equal:Direction.equal explored dir))
              options
          in
          let options =
            List.map
              ~f:(fun (point, dir, uphill) ->
                { path = [ point; dst ]; dir; uphill })
              options
          in
          let options =
            List.filter
              ~f:(fun o -> not (List.mem ~equal:path_equal xs o))
              options
          in
          collapse graph grid (xs @ options))

type state = { last : Point.t; path : Point.t list; weight : int }

let neighbors (graph : graph) (slippery : bool) (s : state) :
    (Point.t * int) list =
  let result = Hashtbl.find_exn graph s.last in
  (* Add the insight about not going up along edges, good description: *)
  (* https://www.reddit.com/r/adventofcode/comments/18oy4pc/comment/kfyvp2g *)
  let result =
    if Int.equal 3 (List.length result) then
      List.filter ~f:(fun e -> not (Direction.equal e.dir UP)) result
    else result
  in
  let result =
    if slippery then List.filter ~f:(fun e -> not e.uphill) result else result
  in
  let result =
    List.filter
      ~f:(fun e -> not (List.mem ~equal:Point.equal s.path e.point))
      result
  in
  List.map ~f:(fun e -> (e.point, e.length)) result

let search (graph : graph) (start : Point.t) (target : Point.t)
    (slippery : bool) : int =
  let rec run (states : state list) (max : int) : int =
    match states with
    | [] -> max
    | s :: xs -> (
        match Point.equal target s.last with
        | true -> run xs (Int.max max s.weight)
        | false ->
            let additional =
              List.map
                ~f:(fun ((p, w) : Point.t * int) : state ->
                  { last = p; path = p :: s.path; weight = s.weight + w })
                (neighbors graph slippery s)
            in
            run (additional @ xs) max)
  in
  run [ { last = start; path = [ start ]; weight = 0 } ] 0

let solution () =
  let grid = Reader.read_grid () in
  let start = Point.move (Grid.min grid) RIGHT 1 in
  let target = Point.move (Grid.max grid) LEFT 1 in

  let graph = Hashtbl.create (module Point) in
  let trace = { path = [ start ]; dir = DOWN; uphill = false } in
  let graph = collapse graph grid [ trace ] in

  let search = search graph start target in
  let part1 = search true in
  let part2 = search false in
  Answer.part1 2154 part1 string_of_int;
  Answer.part2 6654 part2 string_of_int

let () = Answer.timer solution
