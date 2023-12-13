let rec gcd a b = if b = 0 then a else gcd b (a mod b)
let lcm_pair a b = a * b / gcd a b

let lcm values =
  let rec calculate_lcm current values =
    match values with
    | x :: xs -> calculate_lcm (lcm_pair current x) xs
    | [] -> current
  in
  calculate_lcm (List.hd values) (List.tl values)
