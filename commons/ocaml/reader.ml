open Core

let get_year_day executable =
  let parts = String.split ~on:'/' executable in
  let name = List.last_exn parts in
  String.lsplit2_exn name ~on:'_'

let get_filename () =
  let test = ref false in
  let speclist = [ ("--test", Arg.Set test, "Test mode") ] in
  Arg.parse speclist print_endline "";
  if !test then "sample" else "data"

let get_filepath () =
  let year, day = get_year_day (Sys.get_argv ()).(0) in
  let filename = get_filename () in
  String.concat ~sep:"/" [ year; day; filename ^ ".txt" ]

let read () : string =
  let filepath = get_filepath () in
  In_channel.read_all filepath

let read_groups () : string list list =
  let data = read () in
  let groups = Str.split (Str.regexp "\n\n") data in
  List.map ~f:String.split_lines groups

let read_lines () : string list =
  let filepath = get_filepath () in
  In_channel.read_lines filepath

let read_ints () : int list =
  let lines = read_lines () in
  List.map ~f:int_of_string lines

let read_grid () : Grid.t =
  let lines = read_lines () in
  Grid.parse_grid lines
