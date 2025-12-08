open Aoc
open Core

let%expect_test "neighbors" =
  let p : Point.t = { x = -1; y = 3 } in
  let print_neighbor neighbor =
    let as_sexp = [%sexp_of: Direction.t * Point.t] neighbor in
    print_endline (Sexp.to_string as_sexp)
  in
  List.iter ~f:print_neighbor (Point.neighbors p);
  [%expect
    {| 
    (UP((x -1)(y 2)))
    (DOWN((x -1)(y 4)))
    (LEFT((x -2)(y 3)))
    (RIGHT((x 0)(y 3))) |}]
