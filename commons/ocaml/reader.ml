open Point

let get_year_day executable =
  let parts = String.split_on_char '/' executable in
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
  String.concat "/" [ year; day; filename ^ ".txt" ]

let read () : string =
  let filepath = get_filepath () in
  Core.In_channel.read_all filepath

let read_groups () : string list list =
  let data = read () in
  let groups = Str.split (Str.regexp "\n\n") data in
  List.map Core.String.split_lines groups

let read_lines () : string list =
  let filepath = get_filepath () in
  Core.In_channel.read_lines filepath

let read_ints () : int list =
  let lines = read_lines () in
  List.map int_of_string lines

let grid_point (y : int) (x : int) (ch : char) : point * char = ({ x; y }, ch)

let grid_line (y : int) (s : string) : (point * char) list =
  let chars = s |> String.to_seq |> List.of_seq in
  List.mapi (grid_point y) chars

let read_grid () : (point * char) list =
  let lines = read_lines () in
  List.flatten (List.mapi grid_line lines)
