let rec combinations k values =
  if k = 0 then [ [] ]
  else
    match values with
    | x :: xs ->
        let with_x =
          List.map (fun subset -> x :: subset) (combinations (k - 1) xs)
        in
        let without_x = combinations k xs in
        with_x @ without_x
    | [] -> []

let sum values = List.fold_left ( + ) 0 values

let rec valid_combinations k target values =
  let groups = combinations k values in
  let valid_groups = List.filter (fun group -> sum group == target) groups in
  if List.length valid_groups > 0 then valid_groups
  else valid_combinations (k + 1) target values

let entanglement values = List.fold_left ( * ) 1 values

let run values sections =
  let valid_groups = valid_combinations 0 (sum values / sections) values in
  let entanglements = List.map (fun group -> entanglement group) valid_groups in
  let sorted_entanglements = List.sort compare entanglements in
  List.hd sorted_entanglements

let () =
  let values = Aoc.Reader.read_ints () in
  Aoc.Answer.part1 10439961859 (run values 3) string_of_int;
  Aoc.Answer.part2 72050269 (run values 4) string_of_int
