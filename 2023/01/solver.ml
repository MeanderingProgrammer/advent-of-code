let rec find_first index value =
  if index < String.length value then
    match value.[index] with
    | '0' .. '9' as digit -> int_of_char digit - int_of_char '0'
    | _ -> find_first (index + 1) value
  else -1

let rec find_last index value =
  if index >= 0 then
    match value.[index] with
    | '0' .. '9' as digit -> int_of_char digit - int_of_char '0'
    | _ -> find_last (index - 1) value
  else -1

let rec sum result values =
  match values with
  | x :: xs ->
      let current = (10 * find_first 0 x) + find_last (String.length x - 1) x in
      sum (current + result) xs
  | _ -> result

let () =
  let values = Aoc.Reader.read_lines () in
  let part1 = sum 0 values in
  Aoc.Answer.part1 55538 part1 string_of_int
