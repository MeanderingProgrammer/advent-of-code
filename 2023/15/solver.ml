open Aoc
open Core

type operation = Remove of string | Add of string * int

let hash s =
  let rec calculate chars value =
    match chars with
    | x :: xs ->
        let next_value = 17 * (value + int_of_char x) mod 256 in
        calculate xs next_value
    | [] -> value
  in
  calculate (String.to_list s) 0

(* cm- | qp=3 *)
let parse s =
  match String.is_suffix ~suffix:"-" s with
  | true -> Remove (String.sub s ~pos:0 ~len:(String.length s - 1))
  | false -> (
      match String.split ~on:'=' s with
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
      let updated_box = List.Assoc.remove ~equal:String.equal box label in
      Array.set hash_map hash_value updated_box
  | Add (label, value) ->
      let hash_value = hash label in
      let box = Array.get hash_map hash_value in
      let updated_box =
        if List.Assoc.mem ~equal:String.equal box label then
          update box label value
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
  let values = List.mapi ~f:(fun j (_, value) -> (j + 1) * value) box in
  let partial = Util.sum values in
  (i + 1) * partial

let () =
  let data = Reader.read () in
  let values = String.split ~on:',' (String.strip data) in
  let part1 = Util.sum (List.map ~f:hash values) in
  let operations = List.map ~f:parse values in
  let hash_map = Array.create ~len:256 [] in
  run_ops operations hash_map;
  let part2 =
    Util.sum (Array.mapi ~f:focussing_power hash_map |> Array.to_list)
  in
  Answer.part1 514281 part1 string_of_int;
  Answer.part2 244199 part2 string_of_int
