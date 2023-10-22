open Core

let read_lines () = In_channel.read_lines "data.txt"

let read_ints () =
  let lines = read_lines in
  List.map ~f:int_of_string (lines ())
