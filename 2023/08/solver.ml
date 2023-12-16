open Core

type edge = { left : string; right : string }

(* (BBB, CCC) *)
let parse_edge s =
  match Str.split (Str.regexp ", ") s with
  | [ left; right ] ->
      { left = Str.string_after left 1; right = Str.string_before right 3 }
  | _ -> raise (Invalid_argument s)

(* AAA = <edge> *)
let parse_node s =
  match Str.split (Str.regexp " = ") s with
  | [ node; left_right ] -> (node, parse_edge left_right)
  | _ -> raise (Invalid_argument s)

let get_next network direction node =
  let current_edge = List.Assoc.find_exn ~equal:String.equal network node in
  match direction with
  | 'L' -> current_edge.left
  | 'R' -> current_edge.right
  | _ -> raise (Invalid_argument (String.make 1 direction))

let rec follow directions network location =
  match directions with
  | x :: xs ->
      let next_location = get_next network x location in
      follow xs network next_location
  | [] -> location

let rec follow_until i target directions network location =
  if target location then i * List.length directions
  else
    let next_location = follow directions network location in
    follow_until (i + 1) target directions network next_location

let is_zzz s = String.equal s "ZZZ"
let ends ch s = String.is_suffix ~suffix:ch s

let () =
  let groups = Aoc.Reader.read_groups () in
  let directions = List.nth_exn (List.nth_exn groups 0) 0 |> String.to_list in
  let network = List.map ~f:parse_node (List.nth_exn groups 1) in
  let part1 = follow_until 0 is_zzz directions network "AAA" in
  let all_nodes = List.map ~f:(fun (node, _) -> node) network in
  let starts = List.filter ~f:(ends "A") all_nodes in
  let loops =
    List.map ~f:(follow_until 0 (ends "Z") directions network) starts
  in
  let part2 = Aoc.Math.lcm loops in
  Aoc.Answer.part1 24253 part1 string_of_int;
  Aoc.Answer.part2 12357789728873 part2 string_of_int
