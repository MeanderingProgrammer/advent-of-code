(* 0 3 6 9 12 15 *)
let parse_numbers s =
  let numbers = String.split_on_char ' ' s in
  List.map int_of_string numbers

let rec get_diffs numbers =
  match numbers with a :: b :: xs -> (b - a) :: get_diffs (b :: xs) | _ -> []

let rec get_diffs_until_0 numbers =
  if List.for_all (Int.equal 0) numbers then []
  else numbers :: get_diffs_until_0 (get_diffs numbers)

let get_last numbers =
  let index = List.length numbers - 1 in
  List.nth numbers index

let get_first i numbers =
  let value = List.nth numbers 0 in
  if i mod 2 == 0 then value else value * -1

let get_missing last numbers =
  let non_zero_diffs = get_diffs_until_0 numbers in
  let values =
    if last then List.map get_last non_zero_diffs
    else List.mapi get_first non_zero_diffs
  in
  List.fold_left ( + ) 0 values

let () =
  let values = Aoc.Reader.read_lines () in
  let all_numbers = List.map parse_numbers values in
  let missing_last = List.map (get_missing true) all_numbers in
  let part1 = List.fold_left ( + ) 0 missing_last in
  let missing_first = List.map (get_missing false) all_numbers in
  let part2 = List.fold_left ( + ) 0 missing_first in
  Aoc.Answer.part1 1916822650 part1 string_of_int;
  Aoc.Answer.part2 966 part2 string_of_int
