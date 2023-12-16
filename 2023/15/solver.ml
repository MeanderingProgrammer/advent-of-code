type operation = Remove of string | Add of string * int

let rec print_it values =
  match values with
  | [] -> Printf.printf "done\n"
  | x :: xs ->
      (match x with
      | Remove label -> Printf.printf "REMOVE: %s\n" label
      | Add (label, length) -> Printf.printf "ADD: %s %d\n" label length);
      print_it xs

let hash s =
  let rec calculate chars value =
    match chars with
    | x :: xs ->
        let next_value = 17 * (value + int_of_char x) mod 256 in
        calculate xs next_value
    | [] -> value
  in
  calculate (String.to_seq s |> List.of_seq) 0

(* cm- | qp=3 *)
let parse s =
  match String.ends_with ~suffix:"-" s with
  | true -> Remove (String.sub s 0 (String.length s - 1))
  | false -> (
      match String.split_on_char '=' s with
      | [ label; length ] -> Add (label, int_of_string length)
      | _ -> raise (Invalid_argument s))

let () =
  let data = Aoc.Reader.read () in
  let values = String.split_on_char ',' (String.trim data) in
  let part1 = List.fold_left ( + ) 0 (List.map hash values) in
  let operations = List.map parse values in
  print_it operations;
  Aoc.Answer.part1 514281 part1 string_of_int
