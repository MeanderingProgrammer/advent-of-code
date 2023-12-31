open Core

(* Time: <numbers> *)
let parse_values s =
  match String.split ~on:':' s with
  | [ _; numbers ] -> Aoc.Util.parse_numbers numbers
  | _ -> raise (Invalid_argument s)

let rec variants time found max_time record_distance =
  if time < max_time then
    let distance = time * (max_time - time) in
    let next_found = if distance > record_distance then found + 1 else found in
    variants (time + 1) next_found max_time record_distance
  else found

let count_variants time_distance =
  let time, distance = time_distance in
  variants 1 0 time distance

let join values =
  let string_values = List.map ~f:string_of_int values in
  int_of_string (String.concat ~sep:"" string_values)

let () =
  let values = Aoc.Reader.read_lines () in
  let times = parse_values (List.nth_exn values 0) in
  let distances = parse_values (List.nth_exn values 1) in
  let time_distances = List.zip_exn times distances in
  let winning_variants = List.map ~f:count_variants time_distances in
  let part1 = Aoc.Util.multiply winning_variants in
  let part2 = count_variants (join times, join distances) in
  Aoc.Answer.part1 140220 part1 string_of_int;
  Aoc.Answer.part2 39570185 part2 string_of_int
