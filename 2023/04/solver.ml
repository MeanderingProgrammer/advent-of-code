open Core

let is_valid s = not (String.is_empty (String.strip s))

(*  83 86  6 31 17  9 48 53 *)
let parse_numbers s =
  let split = String.split s ~on:' ' in
  let filtered = List.filter ~f:is_valid split in
  List.map ~f:int_of_string filtered

type card = { winning : int list; found : int list }

(* <winning> | <found> *)
let parse_card_numbers s =
  match String.split s ~on:'|' with
  | [ winning; found ] ->
      { winning = parse_numbers winning; found = parse_numbers found }
  | _ -> raise (Invalid_argument s)

(* Card 1: <card_numbers> *)
let parse_card s =
  match String.split s ~on:':' with
  | [ _; card_numbers ] -> parse_card_numbers card_numbers
  | _ -> raise (Invalid_argument s)

let rec match_count result winning found =
  match found with
  | x :: xs ->
      if List.mem ~equal:Int.equal winning x then
        match_count (result + 1) winning xs
      else match_count result winning xs
  | [] -> result

let card_match_count c = match_count 0 c.winning c.found
let score n = if Int.equal n 0 then 0 else Aoc.Math.int_pow 2 (n - 1)

let rec update_counts counts first last amount =
  match counts with
  | x :: xs ->
      let value = if first <= 0 && last >= 0 then x + amount else x in
      value :: update_counts xs (first - 1) (last - 1) amount
  | [] -> []

let rec winnings i matches counts =
  match matches with
  | x :: xs ->
      let count = List.nth_exn counts i in
      winnings (i + 1) xs (update_counts counts (i + 1) (i + x) count)
  | [] -> counts

let () =
  let values = Aoc.Reader.read_lines () in
  let cards = List.map ~f:parse_card values in
  let matches = List.map ~f:card_match_count cards in
  let part1 = Aoc.Util.sum (List.map ~f:score matches) in
  let initial_counts = List.init (List.length matches) ~f:(const 1) in
  let counts = winnings 0 matches initial_counts in
  let part2 = Aoc.Util.sum counts in
  Aoc.Answer.part1 18619 part1 string_of_int;
  Aoc.Answer.part2 8063216 part2 string_of_int
