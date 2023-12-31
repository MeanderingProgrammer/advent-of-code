open Aoc
open Core

let rec combinations k values =
  if k = 0 then [ [] ]
  else
    match values with
    | x :: xs ->
        let with_x =
          List.map ~f:(fun subset -> x :: subset) (combinations (k - 1) xs)
        in
        let without_x = combinations k xs in
        with_x @ without_x
    | [] -> []

let rec valid_combinations k target values =
  let groups = combinations k values in
  let valid_groups =
    List.filter ~f:(fun group -> Int.equal (Util.sum group) target) groups
  in
  if List.length valid_groups > 0 then valid_groups
  else valid_combinations (k + 1) target values

let run values sections =
  let valid_groups = valid_combinations 0 (Util.sum values / sections) values in
  let entanglements =
    List.map ~f:(fun group -> Util.multiply group) valid_groups
  in
  let sorted_entanglements = List.sort ~compare entanglements in
  List.hd_exn sorted_entanglements

let () =
  let values = Reader.read_ints () in
  let part1 = run values 3 in
  let part2 = run values 4 in
  Answer.part1 10439961859 part1 string_of_int;
  Answer.part2 72050269 part2 string_of_int
