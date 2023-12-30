open Core

type point = { x : float; y : float; _z : float }
type stone = { position : point; velocity : point }

(* let stone_string (s : stone) : string = *)
(*   let point_string (p : point) : string = sprintf "(%f, %f)" p.x p.y in *)
(*   sprintf "%s | %s" (point_string s.position) (point_string s.velocity) *)

let parse_float (s : string) : float =
  float_of_int (int_of_string (String.strip s))

(* 19, 13, 30 *)
let parse_point (s : string) : point =
  match Str.split (Str.regexp ", ") s with
  | [ x; y; z ] -> { x = parse_float x; y = parse_float y; _z = parse_float z }
  | _ -> raise (Invalid_argument s)

(* <position> @ <velocity> *)
let parse_stone (s : string) : stone =
  match Str.split (Str.regexp " @ ") s with
  | [ position; velocity ] ->
      { position = parse_point position; velocity = parse_point velocity }
  | _ -> raise (Invalid_argument s)

let pull_xy (p : point) : float * float =
  let { x; y; _ } = p in
  (x, y)

let rec each_pair (s : stone) (ss : stone list) : (stone * stone) list =
  match ss with [] -> [] | x :: xs -> (s, x) :: each_pair s xs

let rec all_pairs (ss : stone list) : (stone * stone) list =
  match ss with [] -> [] | x :: xs -> each_pair x xs @ all_pairs xs

let get_intersection (min : float) (max : float) ((st1, st2) : stone * stone) :
    bool =
  (* printf "%s -> %s\n" (stone_string st1) (stone_string st2); *)
  let (x1, y1), (vx1, vy1) = (pull_xy st1.position, pull_xy st1.velocity) in
  let (x2, y2), (vx2, vy2) = (pull_xy st2.position, pull_xy st2.velocity) in
  (* y1 - y2 - vy2((x1 - x2)/vx2) = (vy2(vx1/vx2) - vy1)t1 *)
  let lhs1 = y1 -. y2 -. (vy2 *. ((x1 -. x2) /. vx2)) in
  let rhs1 = (vy2 *. (vx1 /. vx2)) -. vy1 in
  (* y2 - y1 - vy1((x2 - x1)/vx1) = (vy1(vx2/vx1) - vy2)t2 *)
  let lhs2 = y2 -. y1 -. (vy1 *. ((x2 -. x1) /. vx1)) in
  let rhs2 = (vy1 *. (vx2 /. vx1)) -. vy2 in
  match rhs1 with
  | 0. -> false
  | _ -> (
      let t1 = lhs1 /. rhs1 in
      let t2 = lhs2 /. rhs2 in
      (* printf "L = %f; R = %f; t1 = %f t2 = %f\n" lhs1 rhs1 t1 t2; *)
      match Float.compare t1 0. < 0 || Float.compare t2 0. < 0 with
      | true -> false
      | false ->
          (* x = x1 + vx1(t1) *)
          let x : float = x1 +. (vx1 *. t1) in
          (* y = y1 + vy1(t1) *)
          let y : float = y1 +. (vy1 *. t1) in
          (* printf "%f, %f\n" x y; *)
          let res =
            if not (Float.between ~low:min ~high:max x) then false
            else if not (Float.between ~low:min ~high:max y) then false
            else true
          in
          (* printf "%f, %f: %b\n" x y res; *)
          res)

let () =
  let values = Aoc.Reader.read_lines () in
  let stones = List.map ~f:parse_stone values in
  let pairs = all_pairs stones in
  let part1 =
    List.count ~f:(get_intersection 200000000000000. 400000000000000.) pairs
  in
  Aoc.Answer.part1 14672 part1 string_of_int
