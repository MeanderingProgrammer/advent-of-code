open Core

let increases values =
  let rec f acc values =
    match values with
    | x1 :: x2 :: xs ->
        if x2 > x1 then f (acc + 1) (x2 :: xs) else f acc (x2 :: xs)
    | _ -> acc
  in
  f 0 values

let winsorize values =
  let rec f acc values =
    match values with
    | x1 :: x2 :: x3 :: xs -> f ((x1 + x2 + x3) :: acc) (x2 :: x3 :: xs)
    | _ -> acc
  in
  f [] values

let () =
  let values = Aoc.Reader.read_ints () in
  let part1 = increases values in
  let part2 = increases (List.rev (winsorize values)) in
  Aoc.Answer.part1 1292 part1 string_of_int;
  Aoc.Answer.part2 1262 part2 string_of_int
