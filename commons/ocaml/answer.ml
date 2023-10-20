exception Invalid_input

let part n expected actual f =
  if expected != actual then (
    Printf.printf "Part %d: expected %s found %s\n" n (f expected) (f actual);
    raise Invalid_input)
  else Printf.printf "Part %d: %s\n" n (f actual)

let part1 expected actual f = part 1 expected actual f
let part2 expected actual f = part 2 expected actual f
