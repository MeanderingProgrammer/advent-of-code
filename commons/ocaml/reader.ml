let get_year_day executable =
  let parts = Core.String.split executable ~on:'/' in
  let name = Core.List.last_exn parts in
  Core.String.lsplit2_exn name ~on:'_'

let get_filename () =
  let test = ref false in
  let speclist = [ ("--test", Arg.Set test, "Test mode") ] in
  Arg.parse speclist print_endline "";
  if !test then "sample" else "data"

let get_filepath () =
  let year, day = get_year_day (Core.Sys.get_argv ()).(0) in
  let filename = get_filename () in
  Core.String.concat ~sep:"/" [ year; day; filename ^ ".txt" ]

let read () : string =
  let filepath = get_filepath () in
  Core.In_channel.read_all filepath

let read_groups () : string list list =
  let data = read () in
  let groups = Str.split (Str.regexp "\n\n") data in
  Core.List.map ~f:Core.String.split_lines groups

let read_lines () : string list =
  let filepath = get_filepath () in
  Core.In_channel.read_lines filepath

let read_ints () : int list =
  let lines = read_lines () in
  Core.List.map ~f:int_of_string lines
