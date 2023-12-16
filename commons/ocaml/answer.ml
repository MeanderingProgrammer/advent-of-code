let part n expected actual f =
  match expected == actual with
  | true -> Printf.printf "Part %d: %s\n" n (f actual)
  | false ->
      let error_message =
        Printf.sprintf "Part %d: expected %s found %s" n (f expected) (f actual)
      in
      raise (Invalid_argument error_message)

let part1 expected actual f = part 1 expected actual f
let part2 expected actual f = part 2 expected actual f
