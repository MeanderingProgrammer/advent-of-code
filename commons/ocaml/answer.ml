exception Invalid_input

let part n expected result f =
    if expected != result then raise Invalid_input
    else let value = f result in
        Printf.printf "Part %d: %s\n" n value

let part1 expected result f =
    part 1 expected result f

let part2 expected result f =
    part 2 expected result f
