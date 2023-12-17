open Core

let valid_adjacent grid location =
  let pipe = List.Assoc.find_exn ~equal:Aoc.Point.equal grid location in
  let valid_directions =
    match pipe with
    | '|' -> [ Aoc.Direction.UP; DOWN ]
    | '-' -> [ LEFT; RIGHT ]
    | 'L' -> [ UP; RIGHT ]
    | 'J' -> [ UP; LEFT ]
    | '7' -> [ DOWN; LEFT ]
    | 'F' -> [ DOWN; RIGHT ]
    | _ -> raise (Invalid_argument (String.make 1 pipe))
  in
  let locations = Aoc.Point.adjacent location in
  let valid_locations =
    List.filter
      ~f:(fun (direction, _) ->
        List.exists ~f:(Aoc.Direction.equal direction) valid_directions)
      locations
  in
  List.map ~f:(fun (_, location) -> location) valid_locations

let rec traverse grid steps locations seen =
  let seen = List.map ~f:(fun location -> (location, steps)) locations @ seen in
  let next_locations =
    List.concat (List.map ~f:(valid_adjacent grid) locations)
  in
  let next_locations =
    List.filter
      ~f:(fun location ->
        Option.is_none (List.Assoc.find ~equal:Aoc.Point.equal seen location))
      next_locations
  in
  if List.is_empty next_locations then seen
  else traverse grid (steps + 1) next_locations seen

let increment point_values previous point =
  match List.Assoc.find ~equal:Aoc.Point.equal point_values point with
  | None -> false
  | Some v -> (
      match v with
      | '|' -> true
      | 'J' -> Char.equal 'F' previous
      | '7' -> Char.equal 'L' previous
      | _ -> false)

let rec count_walls point_values previous y x_values =
  match x_values with
  | [] -> 0
  | x :: xs ->
      let point = { Aoc.Point.x; y } in
      let next =
        match List.Assoc.find ~equal:Aoc.Point.equal point_values point with
        | None -> previous
        | Some v -> if Char.equal '-' v then previous else v
      in
      let value = if increment point_values previous point then 1 else 0 in
      value + count_walls point_values next y xs

let point_contained point_values xs point =
  let after = List.filter ~f:(fun x -> x > point.Aoc.Point.x) xs in
  let walls_after = count_walls point_values '|' point.Aoc.Point.y after in
  Int.equal (walls_after mod 2) 1

let contained grid points =
  let not_in point = not (List.mem ~equal:Aoc.Point.equal points point) in
  let possible, _ = List.unzip grid in
  let possible = List.filter ~f:not_in possible in
  let max_x = Aoc.Util.max (List.map ~f:(fun p -> p.Aoc.Point.x) points) in
  let xs = List.init (max_x + 1) ~f:(fun x -> x) in
  let point_values =
    List.map
      ~f:(fun p -> (p, List.Assoc.find_exn ~equal:Aoc.Point.equal grid p))
      points
  in
  List.count ~f:(point_contained point_values xs) possible

let () =
  let grid = Aoc.Reader.read_grid () in
  let start, _ = List.find_exn ~f:(fun (_, ch) -> Char.equal ch 'S') grid in
  let grid =
    (start, 'F') :: List.Assoc.remove ~equal:Aoc.Point.equal grid start
  in
  let point_distances = traverse grid 0 [ start ] [] in
  let points, distances = List.unzip point_distances in
  let part1 = Aoc.Util.max distances in
  let part2 = contained grid points in
  Aoc.Answer.part1 6690 part1 string_of_int;
  Aoc.Answer.part2 525 part2 string_of_int
