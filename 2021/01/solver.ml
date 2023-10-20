let part1 values = 
    let rec f acc values = match values with
        | v1 :: vs -> (
            match vs with
                | v2 :: _ -> if v2 > v1 
                    then f (acc + 1) vs
                    else f acc vs
                | [] -> acc
        )
        | [] -> acc
    in f 0 values


let () = 
    let values = Aoc.Reader.read_ints in
        Aoc.Answer.part1 1292 (part1 values) string_of_int
