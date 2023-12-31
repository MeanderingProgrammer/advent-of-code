open Aoc
open Core

type range = { first : int; last : int }
type condition = { category : char; range : range }
type workflow = { condition : condition option; destination : string }
type rule = string * workflow list
type part = (char * int) list
type part_range = (char * range) list

(* {...} | ...} *)
let remove_bracket (s : string) : string =
  let offset = if String.is_prefix ~prefix:"{" s then 1 else 0 in
  String.sub s ~pos:offset ~len:(String.length s - (1 + offset))

(* <2006 *)
let parse_range (c : char) (value : int) : range =
  match c with
  | '<' -> { first = 1; last = value - 1 }
  | '>' -> { first = value + 1; last = 4000 }
  | _ -> raise (Invalid_argument (Char.to_string c))

(* a<range> *)
let parse_condition (s : string) : condition =
  {
    category = String.get s 0;
    range =
      parse_range (String.get s 1)
        (int_of_string (String.sub s ~pos:2 ~len:(String.length s - 2)));
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
  | Some c ->
      let value = List.Assoc.find_exn ~equal:Char.equal p c.category in
      value >= c.range.first && value <= c.range.last

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

let part_value (p : part) : int = Util.sum (List.map ~f:(fun (_, v) -> v) p)

let combinations (p : part_range) : int =
  Util.multiply (List.map ~f:(fun (_, r) -> r.last - r.first + 1) p)

let rec find_overlap (p : part_range) (workflows : workflow list) =
  match workflows with
  | [] -> []
  | x :: xs -> (
      match x.condition with
      | None -> (x.destination, p) :: find_overlap p xs
      | Some c ->
          let r = List.Assoc.find_exn ~equal:Char.equal p c.category in
          let p = List.Assoc.remove ~equal:Char.equal p c.category in
          let overlap : range =
            {
              first = Int.max r.first c.range.first;
              last = Int.min r.last c.range.last;
            }
          in
          let overlap_p =
            List.Assoc.add ~equal:Char.equal p c.category overlap
          in
          let remainder =
            if r.first < c.range.first then { r with last = c.range.first - 1 }
            else { r with first = c.range.last + 1 }
          in
          let remainder_p =
            List.Assoc.add ~equal:Char.equal p c.category remainder
          in
          (x.destination, overlap_p) :: find_overlap remainder_p xs)

let rec split_ranges (rules : rule list) (pending : (string * part_range) list)
    =
  match pending with
  | [] -> []
  | (name, p) :: xs -> (
      match name with
      | "A" -> p :: split_ranges rules xs
      | "R" -> split_ranges rules xs
      | _ ->
          let workflows = List.Assoc.find_exn ~equal:String.equal rules name in
          let pending = find_overlap p workflows in
          split_ranges rules (pending @ xs))

let () =
  let groups = Reader.read_groups () in
  let rules = List.map ~f:parse_rule (List.nth_exn groups 0) in
  let parts = List.map ~f:parse_part (List.nth_exn groups 1) in
  let accepted_parts = List.filter ~f:(accepted rules "in") parts in
  let part1 = Util.sum (List.map ~f:part_value accepted_parts) in
  let full_range : range = { first = 1; last = 4000 } in
  let initial_range : part_range =
    [
      ('x', full_range); ('m', full_range); ('a', full_range); ('s', full_range);
    ]
  in
  let ranges = split_ranges rules [ ("in", initial_range) ] in
  let part2 = Util.sum (List.map ~f:combinations ranges) in
  Answer.part1 409898 part1 string_of_int;
  Answer.part2 113057405770956 part2 string_of_int
