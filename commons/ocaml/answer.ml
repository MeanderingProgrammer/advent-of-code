open Core

let timer (f : unit -> unit) =
  let start_time = Time_ns.now () in
  f ();
  let end_time = Time_ns.now () in
  let elapsed = Time_ns.diff end_time start_time in
  Printf.printf "Runtime (ns): %d\n" (Time_ns.Span.to_int_ns elapsed)

let part (n : int) (expected : string) (actual : string) =
  match String.equal expected actual with
  | true -> Printf.printf "Part %d: %s\n" n actual
  | false ->
      let error_message =
        Printf.sprintf "Part %d: expected %s found %s" n expected actual
      in
      raise (Invalid_argument error_message)

let part1 (expected : 'a) (actual : 'a) (f : 'a -> string) =
  part 1 (f expected) (f actual)

let part2 (expected : 'a) (actual : 'a) (f : 'a -> string) =
  part 2 (f expected) (f actual)
