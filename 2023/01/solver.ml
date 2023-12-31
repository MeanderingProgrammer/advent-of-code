open Aoc
open Core

let rec find_matching mapping value index =
  match mapping with
  | (k, v) :: xs ->
      if index + String.length k <= String.length value then
        let substring = String.sub value ~pos:index ~len:(String.length k) in
        if String.equal substring k then Some v
        else find_matching xs value index
      else find_matching xs value index
  | [] -> None

let rec find_first mapping value index increment =
  if index >= 0 && index < String.length value then
    match find_matching mapping value index with
    | Some v -> v
    | None -> find_first mapping value (index + increment) increment
  else -1

let rec score mapping values result =
  match values with
  | x :: xs ->
      let first = find_first mapping x 0 1 in
      let second = find_first mapping x (String.length x - 1) (-1) in
      let current = (10 * first) + second in
      score mapping xs (current + result)
  | _ -> result

let () =
  let values = Reader.read_lines () in
  let digit_mapping =
    [
      ("0", 0);
      ("1", 1);
      ("2", 2);
      ("3", 3);
      ("4", 4);
      ("5", 5);
      ("6", 6);
      ("7", 7);
      ("8", 8);
      ("9", 9);
    ]
  in
  let word_mapping =
    [
      ("one", 1);
      ("two", 2);
      ("three", 3);
      ("four", 4);
      ("five", 5);
      ("six", 6);
      ("seven", 7);
      ("eight", 8);
      ("nine", 9);
    ]
  in
  let part1 = score digit_mapping values 0 in
  let part2 = score (word_mapping @ digit_mapping) values 0 in
  Answer.part1 55538 part1 string_of_int;
  Answer.part2 54875 part2 string_of_int
