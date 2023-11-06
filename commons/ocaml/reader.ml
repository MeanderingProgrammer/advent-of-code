open Core

let get_year_day executable =
  let parts = String.split executable ~on:'/' in
  let name = List.last_exn parts in
  String.lsplit2_exn name ~on:'_'

let get_filename () =
  let test = ref false in
  let speclist = [ ("--test", Arg.Set test, "Test mode") ] in
  Arg.parse speclist print_endline "";
  if !test then "sample" else "data"

let read_lines () =
  let year, day = get_year_day (Sys.get_argv ()).(0) in
  let filename = get_filename () in
  let filepath = String.concat ~sep:"/" [ year; day; filename ^ ".txt" ] in
  In_channel.read_lines filepath

let read_ints () =
  let lines = read_lines in
  List.map ~f:int_of_string (lines ())
