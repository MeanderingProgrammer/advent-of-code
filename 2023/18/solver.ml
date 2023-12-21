open Core
open Printf

type plan = { direction : Aoc.Direction.t; amount : int; color : string }

let plan_string (p : plan) : string =
  sprintf "%s %d %s" (Aoc.Direction.to_string p.direction) p.amount p.color

(* U *)
let parse_direction (s : string) : Aoc.Direction.t =
  match s with
  | "U" -> UP
  | "D" -> DOWN
  | "L" -> LEFT
  | "R" -> RIGHT
  | _ -> raise (Invalid_argument s)

(* <direction> 6 (#70c710) *)
let parse_plan (s : string) : plan =
  match String.split s ~on:' ' with
  | [ direction; amount; color ] ->
      {
        direction = parse_direction direction;
        amount = int_of_string amount;
        color = String.sub color ~pos:2 ~len:(String.length color - 3);
      }
  | _ -> raise (Invalid_argument s)

let follow_plan (point : Aoc.Point.t) (p : plan) =
  let rec helper (point : Aoc.Point.t) (direction : Aoc.Direction.t)
      (amount : int) : Aoc.Point.t list =
    match Int.equal amount 0 with
    | true -> []
    | false ->
        let next =
          match direction with
          | UP -> { point with y = point.y - 1 }
          | DOWN -> { point with y = point.y + 1 }
          | LEFT -> { point with x = point.x - 1 }
          | RIGHT -> { point with x = point.x + 1 }
        in
        printf "P = %s\n" (Aoc.Point.to_string next);
        next :: helper next direction (amount - 1)
  in
  helper point p.direction p.amount

let rec follow (current : Aoc.Point.t) (explored : Aoc.Point.t list)
    (plans : plan list) : Aoc.Point.t list =
  match plans with
  | [] -> explored
  | x :: xs ->
      let additional = follow_plan current x in
      let next = List.last_exn additional in
      follow next (additional @ explored) xs

let () =
  let values = Aoc.Reader.read_lines () in
  let plans = List.map ~f:parse_plan values in
  printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:plan_string plans));
  let start : Aoc.Point.t = { x = 0; y = 0 } in
  let points = follow start [ start ] plans in
  printf "RES = %s\n"
    (String.concat ~sep:"\n" (List.map ~f:Aoc.Point.to_string points));
  Aoc.Answer.part1 1 1 string_of_int
