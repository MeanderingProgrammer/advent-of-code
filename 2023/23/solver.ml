open Aoc
open Core

type step = { direction : Direction.t; point : Point.t }
type path = { steps : step list; uphill : bool }

type edge = {
  direction : Direction.t;
  dst : Point.t;
  length : int;
  uphill : bool;
}

type graph = (Point.t, edge list) Hashtbl.t

let path_equal (p1 : path) (p2 : path) : bool =
  let step_equal (s1 : step) (s2 : step) : bool =
    Point.equal s1.point s2.point
  in
  List.equal step_equal p1.steps p2.steps

let valid_space (grid : Grid.t) (s : step) : bool =
  match Hashtbl.find grid s.point with
  | None -> false
  | Some ch -> not (Char.equal '#' ch)

let unseen (path : path) (s : step) : bool =
  let points = List.map ~f:(fun s -> s.point) path.steps in
  not (List.mem ~equal:Point.equal points s.point)

let goes_uphill (previous : char) (s : step) : bool =
  match previous with
  | '^' -> not (Direction.equal UP s.direction)
  | 'v' -> not (Direction.equal DOWN s.direction)
  | '<' -> not (Direction.equal LEFT s.direction)
  | '>' -> not (Direction.equal RIGHT s.direction)
  | _ -> false

let neighbors (grid : Grid.t) (path : path) : (step * bool) list =
  let current = (List.hd_exn path.steps).point in
  (* Continue path in all directions from last point on our path *)
  let result = Point.adjacent current in
  let result =
    List.map ~f:(fun (direction, point) -> { direction; point }) result
  in
  (* Remove anything that's off the grid or goes into a forest *)
  let result = List.filter ~f:(valid_space grid) result in
  (* Remove direction going back the way we traveled if there's at most one other option *)
  let result =
    match List.length result > 2 with
    | true -> result
    | false -> List.filter ~f:(unseen path) result
  in
  (* Add information about whether the step went uphill *)
  let location = Hashtbl.find_exn grid current in
  List.zip_exn result (List.map ~f:(goes_uphill location) result)

(* Lots of this grid is single option moves, this method attemps to *)
(* collapse all of this information into a dense representation *)
let rec collapse (graph : graph) (grid : Grid.t) (paths : path list) : graph =
  match paths with
  | [] -> graph
  | x :: xs -> (
      let options = neighbors grid x in
      match List.length options with
      | 1 ->
          let step, uphill = List.hd_exn options in
          let path = { steps = step :: x.steps; uphill = uphill || x.uphill } in
          collapse graph grid (path :: xs)
      | _ ->
          let steps = List.rev x.steps in
          let src = (List.hd_exn steps).point in
          let dst = List.last_exn steps in
          (* Add current edge to the graph *)
          let edge =
            {
              direction = (List.nth_exn steps 1).direction;
              dst = dst.point;
              length = List.length steps - 1;
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
            match Hashtbl.find graph dst.point with
            | None -> []
            | Some es -> List.map ~f:(fun e -> e.direction) es
          in
          let options =
            List.filter
              ~f:(fun o ->
                not (List.mem ~equal:Direction.equal explored (fst o).direction))
              options
          in
          let options =
            List.map
              ~f:(fun o -> { steps = [ fst o; dst ]; uphill = snd o })
              options
          in
          let options =
            List.filter
              ~f:(fun o -> not (List.mem ~equal:path_equal xs o))
              options
          in
          collapse graph grid (xs @ options))

type node = { last : Point.t; path : Point.t list }
type state = { node : node; weight : int }

let neighbors (graph : graph) (slippery : bool) (n : node) :
    (Point.t * int) list =
  let result = Hashtbl.find_exn graph n.last in
  (* Add the insight about not going up along edges, good description: *)
  (* https://www.reddit.com/r/adventofcode/comments/18oy4pc/comment/kfyvp2g *)
  let result =
    if Int.equal 3 (List.length result) then
      List.filter ~f:(fun e -> not (Direction.equal e.direction UP)) result
    else result
  in
  let result =
    if slippery then List.filter ~f:(fun e -> not e.uphill) result else result
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

let solution () =
  let grid = Reader.read_grid () in
  let start = Point.move (Grid.min grid) RIGHT 1 in
  let target = Point.move (Grid.max grid) LEFT 1 in

  let graph = Hashtbl.create (module Point) in
  let steps = [ { direction = DOWN; point = start } ] in
  let graph = collapse graph grid [ { steps; uphill = false } ] in

  let search = search graph start target in
  let part1 = search true in
  let part2 = search false in
  Answer.part1 2154 part1 string_of_int;
  Answer.part2 6654 part2 string_of_int

let () = Answer.timer solution
