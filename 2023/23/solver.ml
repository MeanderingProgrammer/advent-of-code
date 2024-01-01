open Aoc
open Core

type step = Direction.t * Point.t
type option = step * bool
type path = { traversed : step list; uphill : bool }

type edge = {
  direction : Direction.t;
  dst : Point.t;
  length : int;
  uphill : bool;
}

type graph = (Point.t, edge list) Hashtbl.t

let path_equal (p1 : path) (p2 : path) : bool =
  let step_equal (s1 : step) (s2 : step) : bool =
    Point.equal (snd s1) (snd s2)
  in
  List.equal step_equal p1.traversed p2.traversed

let valid_space (grid : Grid.t) (s : step) : bool =
  match Hashtbl.find grid (snd s) with
  | None -> false
  | Some ch -> not (Char.equal '#' ch)

let unseen (path : path) (s : step) : bool =
  let path = snd (List.unzip path.traversed) in
  not (List.mem ~equal:Point.equal path (snd s))

let goes_uphill (previous : char) (s : step) : bool =
  match previous with
  | '^' -> not (Direction.equal UP (fst s))
  | 'v' -> not (Direction.equal DOWN (fst s))
  | '<' -> not (Direction.equal LEFT (fst s))
  | '>' -> not (Direction.equal RIGHT (fst s))
  | _ -> false

let neighbors (grid : Grid.t) (path : path) : option list =
  let current = snd (List.hd_exn path.traversed) in
  (* Continue path in all directions from last point on our path *)
  let result = Point.adjacent current in
  (* Remove anything that's off the grid or goes into a forest *)
  let result = List.filter ~f:(valid_space grid) result in
  (* Remove direction going back the way we traveled if there's at most one other option *)
  let result =
    if List.length result > 2 then result
    else List.filter ~f:(unseen path) result
  in
  (* Add information about whether the step went uphill *)
  let location = Hashtbl.find_exn grid current in
  List.zip_exn result (List.map ~f:(goes_uphill location) result)

(* Lots of this grid is single option moves, this method attemps to *)
(* collapse all of this information into a dense representation *)
let rec collapse (grid : Grid.t) (graph : graph) (paths : path list) : graph =
  match paths with
  | [] -> graph
  | x :: xs -> (
      let options = neighbors grid x in
      match List.length options with
      | 1 ->
          let step, uphill = List.hd_exn options in
          let path =
            { traversed = step :: x.traversed; uphill = uphill || x.uphill }
          in
          collapse grid graph (path :: xs)
      | _ ->
          let traversed = List.rev x.traversed in
          let src = snd (List.hd_exn traversed) in
          let dst = List.last_exn traversed in
          (* Add current edge to the graph *)
          let edge =
            {
              direction = fst (List.nth_exn traversed 1);
              dst = snd dst;
              length = List.length traversed - 1;
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
            match Hashtbl.find graph (snd dst) with
            | None -> []
            | Some es -> List.map ~f:(fun e -> e.direction) es
          in
          let options =
            List.filter
              ~f:(fun o ->
                not (List.mem ~equal:Direction.equal explored (fst (fst o))))
              options
          in
          let options =
            List.map
              ~f:(fun o -> { traversed = [ fst o; dst ]; uphill = snd o })
              options
          in
          let options =
            List.filter
              ~f:(fun o -> not (List.mem ~equal:path_equal xs o))
              options
          in
          collapse grid graph (xs @ options))

type node = { last : Point.t; path : Point.t list }
type state = { node : node; weight : int }

let neighbors (graph : graph) (slippery : bool) (n : node) :
    (Point.t * int) list =
  let edges = Hashtbl.find_exn graph n.last in
  let result =
    if slippery then List.filter ~f:(fun e -> not e.uphill) edges else edges
  in
  let result =
    List.filter
      ~f:(fun e -> not (List.mem ~equal:Point.equal n.path e.dst))
      result
  in
  List.map ~f:(fun e -> (e.dst, e.length)) result

let search (graph : graph) (start : Point.t) (target : Point.t)
    (slippery : bool) : int =
  let rec run (states : state list) (max : int) : int =
    match states with
    | [] -> max
    | s :: xs -> (
        match Point.equal target s.node.last with
        | true -> run xs (Int.max max s.weight)
        | false ->
            let additional =
              List.map
                ~f:(fun ((p, w) : Point.t * int) : state ->
                  {
                    node = { last = p; path = p :: s.node.path };
                    weight = s.weight + w;
                  })
                (neighbors graph slippery s.node)
            in
            run (additional @ xs) max)
  in
  run [ { node = { last = start; path = [ start ] }; weight = 0 } ] 0

let () =
  let grid = Reader.read_grid () in

  let start : Point.t = { x = 1; y = 0 } in
  let graph = Hashtbl.create (module Point) in
  let start_path = { traversed = [ (DOWN, start) ]; uphill = false } in
  let graph = collapse grid graph [ start_path ] in

  let max = Grid.max grid in
  let target = { max with x = max.x - 1 } in

  let part1 = search graph start target true in
  let part2 = search graph start target false in
  Answer.part1 2154 part1 string_of_int;
  Answer.part2 6654 part2 string_of_int
