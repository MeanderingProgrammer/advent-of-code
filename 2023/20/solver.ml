open Aoc
open Core

type pulse_type = Low | High
type event = { src : string; dst : string; pulse : pulse_type }

type module_state =
  | Broadcast
  | FlipFlop of bool ref
  | Conjunction of (string, pulse_type) Hashtbl.t

type module_info = { state : module_state; receivers : string list }
type module_map = (string, module_info) Hashtbl.t

let is_low (p : pulse_type) : bool = match p with High -> false | Low -> true

let parse_module_info (s : string) : string * module_info =
  match Str.split (Str.regexp " -> ") s with
  | [ role_name; receivers ] ->
      let state =
        match String.get role_name 0 with
        | '%' -> FlipFlop (ref false)
        | '&' -> Conjunction (Hashtbl.create (module String))
        | 'b' -> Broadcast
        | _ -> raise (Invalid_argument role_name)
      in
      let name =
        match state with
        | Broadcast -> "Broadcast"
        | FlipFlop _ | Conjunction _ ->
            String.sub role_name ~pos:1 ~len:(String.length role_name - 1)
      in
      let receivers = Str.split (Str.regexp ", ") receivers in
      (name, { state; receivers })
  | _ -> raise (Invalid_argument s)

let find_inputs (modules : module_map) (target : string) : string list =
  let in_receivers (name : string) : bool =
    let m = Hashtbl.find_exn modules name in
    List.mem ~equal:String.equal m.receivers target
  in
  List.filter ~f:in_receivers (Hashtbl.keys modules)

let rec initialize_conjuctions (modules : module_map) (names : string list) =
  match names with
  | [] -> ()
  | x :: xs ->
      let m = Hashtbl.find_exn modules x in
      (match m.state with
      | Conjunction v ->
          let inputs = find_inputs modules x in
          List.iter ~f:(fun input -> Hashtbl.set v ~key:input ~data:Low) inputs
      | _ -> ());
      initialize_conjuctions modules xs

let get_modules () : module_map =
  let values = Reader.read_lines () in
  let module_infos = List.map ~f:parse_module_info values in
  let modules = Hashtbl.of_alist_exn (module String) module_infos in
  initialize_conjuctions modules (Hashtbl.keys modules);
  modules

let rec process_events (modules : module_map) (f : event -> bool)
    (events : event list) (low : int) (high : int) (matches : bool) :
    int * int * bool =
  match events with
  | [] -> (low, high, matches)
  | x :: xs -> (
      let low, high =
        match x.pulse with Low -> (low + 1, high) | High -> (low, high + 1)
      in
      let matches = matches || f x in
      match Hashtbl.find modules x.dst with
      | None -> process_events modules f xs low high matches
      | Some target ->
          let pulse =
            match target.state with
            | Broadcast -> Some x.pulse
            | FlipFlop v -> (
                match x.pulse with
                | High -> None
                | Low ->
                    v := not !v;
                    Some (if !v then High else Low))
            | Conjunction v ->
                Hashtbl.set v ~key:x.src ~data:x.pulse;
                let num_low = List.count ~f:is_low (Hashtbl.data v) in
                if num_low > 0 then Some High else Some Low
          in
          let events =
            match pulse with
            | None -> []
            | Some p ->
                List.map
                  ~f:(fun m -> { src = x.dst; dst = m; pulse = p })
                  target.receivers
          in
          process_events modules f (List.append xs events) low high matches)

let press_button (modules : module_map) (f : event -> bool) : int * int * bool =
  let initial = { src = "Button"; dst = "Broadcast"; pulse = Low } in
  process_events modules f [ initial ] 0 0 false

let run_for (modules : module_map) (n : int) : int =
  let low = ref 0 in
  let high = ref 0 in
  for _ = 1 to n do
    let d_low, d_high, _ = press_button modules (fun _ -> false) in
    low := !low + d_low;
    high := !high + d_high
  done;
  !low * !high

let rec until_condition (modules : module_map) (f : event -> bool) : int =
  let _, _, matches = press_button modules f in
  match matches with true -> 1 | false -> 1 + until_condition modules f

let until_high (dst : string) (src : string) =
  let condition (e : event) : bool =
    String.equal e.src src && String.equal e.dst dst && not (is_low e.pulse)
  in
  until_condition (get_modules ()) condition

let until_rx_high (modules : module_map) : int =
  let rx_input = List.hd_exn (find_inputs modules "rx") in
  let main_inputs = find_inputs modules rx_input in
  let periods = List.map ~f:(until_high rx_input) main_inputs in
  Util.multiply periods

let () =
  let part1 = run_for (get_modules ()) 1_000 in
  let part2 = until_rx_high (get_modules ()) in
  Answer.part1 818649769 part1 string_of_int;
  Answer.part2 246313604784977 part2 string_of_int
