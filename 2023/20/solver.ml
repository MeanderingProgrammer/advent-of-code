open Core
open Printf

type module_role = Broadcast | FlipFlop | Conjunction
type module_info = { role : module_role; receivers : string list }

let module_info_string (m : module_info) : string =
  let role =
    match m.role with Broadcast -> "B" | FlipFlop -> "F" | Conjunction -> "C"
  in
  sprintf "%s -> %s" role (String.concat ~sep:"," m.receivers)

let parse_module_info (s : string) : string * module_info =
  match Str.split (Str.regexp " -> ") s with
  | [ role_name; receivers ] ->
      let role =
        match String.get role_name 0 with
        | '%' -> FlipFlop
        | '&' -> Conjunction
        | 'b' -> Broadcast
        | _ -> raise (Invalid_argument role_name)
      in
      let name =
        match role with
        | Broadcast -> ""
        | FlipFlop | Conjunction ->
            String.sub role_name ~pos:1 ~len:(String.length role_name - 1)
      in
      printf "%s, %s, %s\n" role_name receivers name;
      (name, { role; receivers = Str.split (Str.regexp ", ") receivers })
  | _ -> raise (Invalid_argument s)

let () =
  let values = Aoc.Reader.read_lines () in
  let module_mapping =
    Hashtbl.of_alist_exn (module String) (List.map ~f:parse_module_info values)
  in
  printf "%s\n" (module_info_string (Hashtbl.find_exn module_mapping ""));
  Aoc.Answer.part1 1 1 string_of_int
