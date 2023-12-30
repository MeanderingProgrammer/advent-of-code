open Core

module Point = struct
  type t = { x : int; y : int; z : int } [@@deriving compare, hash, sexp]
end

type int_set = (int, bool) Hashtbl.t
type grid = (Point.t, int) Hashtbl.t
type falling_point = { x : int; y : int; mutable z : int }
type axis = X | Y | Z

type brick = {
  id : int;
  start : falling_point;
  length : int;
  axis : axis;
  mutable held_by : int list;
}

let on_axis (a : axis) (p : falling_point) : int =
  match a with X -> p.x | Y -> p.y | Z -> p.z

(* 0,0,2 *)
let parse_point (s : string) : falling_point =
  match List.map ~f:int_of_string (String.split ~on:',' s) with
  | [ x; y; z ] -> { x; y; z }
  | _ -> raise (Invalid_argument s)

let get_axis (p1 : falling_point) (p2 : falling_point) : axis =
  match (Int.equal p1.x p2.x, Int.equal p1.y p2.y, Int.equal p1.z p2.z) with
  (* Consider the unit brick to be X aligned, this is arbitrary *)
  | _, true, true -> X
  | true, false, true -> Y
  | true, true, false -> Z
  | _ -> raise (Invalid_argument "Invalid points")

(* <point_1>~<point_2> *)
let parse_brick (i : int) (s : string) : brick =
  match String.split ~on:'~' s with
  | [ p1; p2 ] ->
      let p1, p2 = (parse_point p1, parse_point p2) in
      let axis = get_axis p1 p2 in
      let v1, v2 = (on_axis axis p1, on_axis axis p2) in
      {
        id = i;
        start = (if v1 < v2 then p1 else p2);
        length = Int.max v1 v2 - Int.min v1 v2 + 1;
        axis;
        held_by = [];
      }
  | _ -> raise (Invalid_argument s)

let by_lowest (b1 : brick) (b2 : brick) : int =
  Int.compare b1.start.z b2.start.z

let by_id (b1 : brick) (b2 : brick) : int = Int.compare b1.id b2.id

let add (b : brick) (z : int) (amount : int) : Point.t =
  match b.axis with
  | X -> { x = b.start.x + amount; y = b.start.y; z = b.start.z + z }
  | Y -> { x = b.start.x; y = b.start.y + amount; z = b.start.z + z }
  | Z -> { x = b.start.x; y = b.start.y; z = b.start.z + amount + z }

let to_points (b : brick) (z : int) : Point.t list =
  List.init b.length ~f:(add b z)

let get_held_by (settled : grid) (b : brick) : int list =
  let below = to_points b (-1) in
  let held_by = List.filter_map ~f:(Hashtbl.find settled) below in
  List.dedup_and_sort ~compare:Int.compare held_by

let rec fall (settled : grid) (b : brick) : unit =
  let held_by = get_held_by settled b in
  match Int.equal b.start.z 1 || not (List.is_empty held_by) with
  | true ->
      List.iter
        ~f:(fun point -> Hashtbl.add_exn settled ~key:point ~data:b.id)
        (to_points b 0);
      b.held_by <- held_by
  | false ->
      b.start.z <- b.start.z - 1;
      fall settled b

let unsupported (removed : int_set) (b : brick) : bool =
  Int.equal 0
    (List.count ~f:(fun support -> not (Hashtbl.mem removed support)) b.held_by)

let fall_count (settled : grid) (bricks : brick list) (b : brick) : int =
  let rec helper (removed : int_set) (b : brick) : int =
    Hashtbl.add_exn removed ~key:b.id ~data:true;
    let above = to_points b 1 in
    let holding = List.filter_map ~f:(Hashtbl.find settled) above in
    let holding = List.dedup_and_sort ~compare:Int.compare holding in
    let holding = List.filter ~f:(fun id -> not (Int.equal id b.id)) holding in
    let holding = List.map ~f:(List.nth_exn bricks) holding in
    let would_fall = List.filter ~f:(unsupported removed) holding in
    List.length would_fall
    + Aoc.Util.sum (List.map ~f:(helper removed) would_fall)
  in
  helper (Hashtbl.create (module Int)) b

let () =
  let values = Aoc.Reader.read_lines () in
  let bricks = List.mapi ~f:parse_brick values in
  let bricks = List.sort ~compare:by_lowest bricks in
  let settled = Hashtbl.create (module Point) in
  List.iter ~f:(fall settled) bricks;
  let id_ordered = List.sort ~compare:by_id bricks in
  let fall_counts = List.map ~f:(fall_count settled id_ordered) bricks in
  let part1 = List.count ~f:(Int.equal 0) fall_counts in
  let part2 = Aoc.Util.sum fall_counts in
  Aoc.Answer.part1 519 part1 string_of_int;
  Aoc.Answer.part2 109531 part2 string_of_int
