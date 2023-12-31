open Core

let sum (values : int list) : int = List.fold_left ~f:( + ) ~init:0 values
let multiply (values : int list) : int = List.fold_left ~init:1 ~f:( * ) values

let max (values : int list) : int =
  List.fold_left ~init:(List.hd_exn values) ~f:Int.max (List.tl_exn values)

let min (values : int list) : int =
  List.fold_left ~init:(List.hd_exn values) ~f:Int.min (List.tl_exn values)

let identity (value : 'a) : 'a = value

(*  83 86  6 31 17  9 48 53 *)
let parse_numbers (s : string) : int list =
  let non_empty (s : string) : bool = not (String.is_empty (String.strip s)) in
  let numbers = String.split s ~on:' ' in
  List.map ~f:int_of_string (List.filter ~f:non_empty numbers)
