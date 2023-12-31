open Core

let sum (values : int list) : int = List.fold_left ~f:( + ) ~init:0 values
let multiply (values : int list) : int = List.fold_left ~init:1 ~f:( * ) values

let max (values : int list) : int =
  List.fold_left ~init:(List.hd_exn values) ~f:Int.max (List.tl_exn values)

let min (values : int list) : int =
  List.fold_left ~init:(List.hd_exn values) ~f:Int.min (List.tl_exn values)

let not_equal (s1 : string) (s2 : string) : bool = not (String.equal s1 s2)
let identity (value : 'a) : 'a = value
