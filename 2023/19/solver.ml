open Core
open Printf

type comparison = LESS_THAN | GREATER_THAN
type condition = { category : char; comp : comparison; value : int }
type workflow = { condition : condition option; destination : string }
type rule = string * workflow list
type part = (char * int) list

let comparison_string (c : comparison) : string =
  match c with LESS_THAN -> "<" | GREATER_THAN -> ">"

let condition_string (c : condition) : string =
  sprintf "(%c %s %d)" c.category (comparison_string c.comp) c.value

let workflow_string (w : workflow) : string =
  let condition_str =
    match w.condition with None -> "ALL" | Some c -> condition_string c
  in
  sprintf "%s -> %s" condition_str w.destination

let rule_string ((name, workflows) : rule) : string =
  sprintf "%s -> [%s]" name
    (String.concat ~sep:", " (List.map ~f:workflow_string workflows))

let rec part_string (p : part) : string =
  match p with
  | [] -> ""
  | (c, v) :: xs -> sprintf "(%c, %d), " c v ^ part_string xs

(* {...} | ...} *)
let remove_bracket (s : string) : string =
  let offset = if String.is_prefix ~prefix:"{" s then 1 else 0 in
  String.sub s ~pos:offset ~len:(String.length s - (1 + offset))

(* < | > *)
let parse_comparison (c : char) : comparison =
  match c with
  | '<' -> LESS_THAN
  | '>' -> GREATER_THAN
  | _ -> raise (Invalid_argument (Char.to_string c))

(* a<comparison>2006 *)
let parse_condition (s : string) : condition =
  {
    category = String.get s 0;
    comp = parse_comparison (String.get s 1);
    value = int_of_string (String.sub s ~pos:2 ~len:(String.length s - 2));
  }

(* <condition>:qkq | rfg *)
let parse_workflow (s : string) : workflow =
  match String.split ~on:':' s with
  | [ c; destination ] -> { condition = Some (parse_condition c); destination }
  | [ destination ] -> { condition = None; destination }
  | _ -> raise (Invalid_argument s)

(* px{<workflow_1>,...} *)
let parse_rule (s : string) : rule =
  match String.split ~on:'{' s with
  | [ name; workflows ] ->
      let workflows = remove_bracket workflows in
      let workflows = String.split ~on:',' workflows in
      (name, List.map ~f:parse_workflow workflows)
  | _ -> raise (Invalid_argument s)

(* x=787 *)
let parse_category (s : string) : char * int =
  match String.split ~on:'=' s with
  | [ category; value ] -> (String.get category 0, int_of_string value)
  | _ -> raise (Invalid_argument s)

(* {<category_1>,...} *)
let parse_part (s : string) : part =
  let s = remove_bracket s in
  List.map ~f:parse_category (String.split ~on:',' s)

let matches (c : condition option) (p : part) : bool =
  match c with
  | None -> true
  | Some c -> (
      let value = List.Assoc.find_exn ~equal:Char.equal p c.category in
      match c.comp with
      | LESS_THAN -> value < c.value
      | GREATER_THAN -> value > c.value)

let rec find_matching (workflows : workflow list) (p : part) : string =
  match workflows with
  | [] -> raise (Invalid_argument "No matching worflow")
  | x :: xs ->
      if matches x.condition p then x.destination else find_matching xs p

let rec accepted (rules : rule list) (current : string) (p : part) : bool =
  let workflows = List.Assoc.find_exn ~equal:String.equal rules current in
  let matching = find_matching workflows p in
  match matching with
  | "A" -> true
  | "R" -> false
  | _ -> accepted rules matching p

let part_value (p : part) : int = Aoc.Util.sum (List.map ~f:(fun (_, v) -> v) p)

let () =
  let groups = Aoc.Reader.read_groups () in
  let rules = List.map ~f:parse_rule (List.nth_exn groups 0) in
  let parts = List.map ~f:parse_part (List.nth_exn groups 1) in
  printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:rule_string rules));
  printf "%s\n" (String.concat ~sep:"\n" (List.map ~f:part_string parts));
  let parts = List.filter ~f:(accepted rules "in") parts in
  let part1 = Aoc.Util.sum (List.map ~f:part_value parts) in
  Aoc.Answer.part1 19114 part1 string_of_int
