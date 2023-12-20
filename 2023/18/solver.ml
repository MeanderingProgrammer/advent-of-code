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

let () =
  let values = Aoc.Reader.read_lines () in
  let plans = List.map ~f:parse_plan values in
  printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:plan_string plans));
  Aoc.Answer.part1 1 1 string_of_int
