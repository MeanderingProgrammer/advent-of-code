let increases values =
    let rec f acc values = match values with
        | x1 :: xs -> (
            match xs with
                | x2 :: _ -> if x2 > x1
                    then f (acc + 1) xs
                    else f acc xs
                | [] -> acc
        )
        | [] -> acc
    in f 0 values

let winsorize values =
    let rec f acc values = match values with
        | x1 :: x2 :: x3 :: xs -> f ((x1 + x2 + x3) :: acc) (x2 :: x3 :: xs)
        | _ -> acc
    in f [] values

let () = 
    let values = Aoc.Reader.read_ints in
        Aoc.Answer.part1 1292 (increases values) string_of_int;
        Aoc.Answer.part2 1262 (increases (List.rev (winsorize values))) string_of_int
