let rec print_it values =
  match values with
  | x :: xs ->
      Printf.printf "%s " x;
      print_it xs
  | _ -> Printf.printf "done\n"

let () =
  let values = Aoc.Reader.read_lines () in
  print_it values;
  Aoc.Answer.part1 1 1 string_of_int
