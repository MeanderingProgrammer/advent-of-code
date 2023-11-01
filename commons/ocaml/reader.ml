open Core

let get_year_day executable =
  let parts = String.split executable ~on:'/' in
  let name = List.last_exn parts in
  String.lsplit2_exn name ~on:'_'

let read_lines () =
  let year, day = get_year_day (Sys.get_argv ()).(0) in
  let filename = String.concat ~sep:"/" [ year; day; "data.txt" ] in
  In_channel.read_lines filename

let read_ints () =
  let lines = read_lines in
  List.map ~f:int_of_string (lines ())
