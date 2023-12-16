type operation = Remove of string | Add of string * int

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

let rec update box label value =
  match box with
  | [] -> []
  | (l, v) :: xs ->
      let current = if String.equal label l then (label, value) else (l, v) in
      current :: update xs label value

let run_op operation hash_map =
  match operation with
  | Remove label ->
      let hash_value = hash label in
      let box = Array.get hash_map hash_value in
      let updated_box = List.remove_assoc label box in
      Array.set hash_map hash_value updated_box
  | Add (label, value) ->
      let hash_value = hash label in
      let box = Array.get hash_map hash_value in
      let updated_box =
        if List.mem_assoc label box then update box label value
        else (label, value) :: box
      in
      Array.set hash_map hash_value updated_box

let rec run_ops operations hash_map =
  match operations with
  | [] -> ()
  | x :: xs ->
      run_op x hash_map;
      run_ops xs hash_map

let focussing_power i box =
  let box = List.rev box in
  let values = List.mapi (fun j (_, value) -> (j + 1) * value) box in
  let partial = Aoc.Util.sum values in
  (i + 1) * partial

let () =
  let data = Aoc.Reader.read () in
  let values = String.split_on_char ',' (String.trim data) in
  let part1 = Aoc.Util.sum (List.map hash values) in
  let operations = List.map parse values in
  let hash_map = Array.make 256 [] in
  run_ops operations hash_map;
  let part2 =
    Aoc.Util.sum (Array.mapi focussing_power hash_map |> Array.to_list)
  in
  Aoc.Answer.part1 514281 part1 string_of_int;
  Aoc.Answer.part2 244199 part2 string_of_int
