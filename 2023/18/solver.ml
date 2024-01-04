open Aoc
open Core

type plan = { direction : Direction.t; amount : int }

(* U | D | L | R *)
let parse_direct_dir (s : string) : Direction.t =
  match s with
  | "U" -> UP
  | "D" -> DOWN
  | "L" -> LEFT
  | "R" -> RIGHT
  | _ -> raise (Invalid_argument s)

(* <direction> 6 _ *)
let parse_direct (s : string) : plan =
  match String.split s ~on:' ' with
  | [ direction; amount; _ ] ->
      { direction = parse_direct_dir direction; amount = int_of_string amount }
  | _ -> raise (Invalid_argument s)

(* 0 | 1 | 2 | 3 *)
let parse_color_dir (c : char) : Direction.t =
  match c with
  | '0' -> RIGHT
  | '1' -> DOWN
  | '2' -> LEFT
  | '3' -> UP
  | _ -> raise (Invalid_argument (Char.to_string c))

(* _ _ (#70c710) *)
let parse_color (s : string) : plan =
  match String.split s ~on:' ' with
  | [ _; _; color ] ->
      let direction = String.get color 7 in
      let hex = "0x" ^ String.sub color ~pos:2 ~len:5 in
      { direction = parse_color_dir direction; amount = int_of_string hex }
  | _ -> raise (Invalid_argument s)

let plan_edge (point : Point.t) (p : plan) : Point.t =
  match p.direction with
  | UP -> { point with y = point.y - p.amount }
  | DOWN -> { point with y = point.y + p.amount }
  | LEFT -> { point with x = point.x - p.amount }
  | RIGHT -> { point with x = point.x + p.amount }

let rec plan_edges (current : Point.t) (plans : plan list) : Point.t list =
  match plans with
  | [] -> []
  | x :: xs ->
      let edge = plan_edge current x in
      edge :: plan_edges edge xs

let shoelace (edges : Point.t list) : int =
  let rec helper (edges : Point.t list) : int =
    match edges with
    | p1 :: p2 :: xs ->
        let value = (p1.x * p2.y) - (p2.x * p1.y) in
        let perimeter = Int.abs (p2.x - p1.x + p2.y - p1.y) in
        value + perimeter + helper (p2 :: xs)
    | _ -> 0
  in
  let result = helper edges in
  (result / 2) + 1

let calculate_area (plans : plan list) : int =
  let start : Point.t = { x = 0; y = 0 } in
  let edges = start :: plan_edges start plans in
  shoelace edges

let solution () =
  let values = Reader.read_lines () in
  let direct = List.map ~f:parse_direct values in
  let color = List.map ~f:parse_color values in
  let part1 = calculate_area direct in
  let part2 = calculate_area color in
  Answer.part1 48795 part1 string_of_int;
  Answer.part2 40654918441248 part2 string_of_int

let () = Answer.timer solution
