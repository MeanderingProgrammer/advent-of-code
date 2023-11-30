let rec find_matching mapping index value =
  match mapping with
  | (k, v) :: xs ->
      if index + String.length k <= String.length value then
        let substring = String.sub value index (String.length k) in
        if String.compare substring k == 0 then Some v
        else find_matching xs index value
      else find_matching xs index value
  | [] -> None

let rec find_first mapping index value =
  if index < String.length value then
    match find_matching mapping index value with
    | Some v -> v
    | None -> find_first mapping (index + 1) value
  else -1

let rec find_last mapping index value =
  if index >= 0 then
    match find_matching mapping index value with
    | Some v -> v
    | _ -> find_last mapping (index - 1) value
  else -1

let rec sum mapping result values =
  match values with
  | x :: xs ->
      let current =
        (10 * find_first mapping 0 x)
        + find_last mapping (String.length x - 1) x
      in
      sum mapping (current + result) xs
  | _ -> result

let () =
  let values = Aoc.Reader.read_lines () in
  let part1_mapping =
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
  let part1 = sum part1_mapping 0 values in
  let part2_mapping =
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
  let part2 = sum part2_mapping 0 values in
  Aoc.Answer.part1 55538 part1 string_of_int;
  Aoc.Answer.part2 54875 part2 string_of_int
