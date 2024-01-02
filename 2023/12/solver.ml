open Aoc
open Core

module Row = struct
  type t = { springs : char list; groups : int list }
  [@@deriving compare, hash, sexp]
end

(* 1,1,3 *)
let parse_groups s = List.map ~f:int_of_string (String.split ~on:',' s)

(* ???.### <groups> *)
let parse_row (s : string) : Row.t =
  match String.split ~on:' ' s with
  | [ springs; groups ] ->
      { springs = String.to_list springs; groups = parse_groups groups }
  | _ -> raise (Invalid_argument s)

let group_fits springs group =
  if List.length springs < group then false
  else if
    List.exists ~f:(Char.equal '.')
      (List.filteri ~f:(fun i _ -> i < group) springs)
  then false
  else if
    List.length springs > group && Char.equal (List.nth_exn springs group) '#'
  then false
  else true

let rec count springs groups cache =
  let handle_empty () = count (List.tl_exn springs) groups cache in
  let handle_group group =
    match group_fits springs group with
    | false -> 0
    | true ->
        let next_springs = List.filteri ~f:(fun i _ -> i > group) springs in
        count next_springs (List.tl_exn groups) cache
  in
  let state : Row.t = { springs; groups } in
  match Hashtbl.find cache state with
  | Some value -> value
  | None ->
      let value =
        match springs with
        | [] -> if List.is_empty groups then 1 else 0
        | spring :: _ -> (
            match groups with
            | [] -> if List.mem ~equal:Char.equal springs '#' then 0 else 1
            | group :: _ -> (
                match spring with
                | '.' -> handle_empty ()
                | '#' -> handle_group group
                | '?' -> handle_empty () + handle_group group
                | _ -> raise (Invalid_argument (String.make 1 spring))))
      in
      Hashtbl.set cache ~key:state ~data:value;
      value

let count_folded (r : Row.t) =
  count r.springs r.groups (Hashtbl.create (module Row))

let count_unfolded (r : Row.t) =
  let repeat values n = List.concat (List.init n ~f:(const values)) in
  let springs = List.tl_exn (repeat ([ '?' ] @ r.springs) 5) in
  let groups = repeat r.groups 5 in
  count springs groups (Hashtbl.create (module Row))

let () =
  let values = Reader.read_lines () in
  let rows = List.map ~f:parse_row values in
  let part1 = Util.sum (List.map ~f:count_folded rows) in
  let part2 = Util.sum (List.map ~f:count_unfolded rows) in
  Answer.part1 8075 part1 string_of_int;
  Answer.part2 4232520187524 part2 string_of_int
