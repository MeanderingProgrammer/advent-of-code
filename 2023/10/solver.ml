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

let () =
  let grid = Aoc.Reader.read_grid () in
  let start, _ = List.find_exn ~f:(fun (_, ch) -> Char.equal ch 'S') grid in
  let grid =
    (start, 'F') :: List.Assoc.remove ~equal:Aoc.Point.equal grid start
  in
  let distances = traverse grid 0 [ start ] [] in
  let values = List.map ~f:(fun (_, distance) -> distance) distances in
  let part1 = Aoc.Util.max values in
  Aoc.Answer.part1 6690 part1 string_of_int
