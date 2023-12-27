open Core
open Printf

type point = { x : int; y : int; z : int }
type stone = { position : point; velocity : point }

let point_string (p : point) : string = sprintf "(%d, %d, %d)" p.x p.y p.z

let stone_string (s : stone) : string =
  sprintf "%s | %s" (point_string s.position) (point_string s.velocity)

let parse_int (s : string) : int = int_of_string (String.strip s)

(* 19, 13, 30 *)
let parse_point (s : string) : point =
  match Str.split (Str.regexp ", ") s with
  | [ x; y; z ] -> { x = parse_int x; y = parse_int y; z = parse_int z }
  | _ -> raise (Invalid_argument s)

(* <position> @ <velocity> *)
let parse_stone (s : string) : stone =
  match Str.split (Str.regexp " @ ") s with
  | [ position; velocity ] ->
      { position = parse_point position; velocity = parse_point velocity }
  | _ -> raise (Invalid_argument s)

let () =
  let values = Aoc.Reader.read_lines () in
  let stones = List.map ~f:parse_stone values in
  printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:stone_string stones));
  Aoc.Answer.part1 1 1 string_of_int
