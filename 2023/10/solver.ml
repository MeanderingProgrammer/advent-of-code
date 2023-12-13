open Aoc.Point

let valid_adjacent grid location =
  let pipe = List.assoc location grid in
  let valid_directions =
    match pipe with
    | '|' -> [ UP; DOWN ]
    | '-' -> [ LEFT; RIGHT ]
    | 'L' -> [ UP; RIGHT ]
    | 'J' -> [ UP; LEFT ]
    | '7' -> [ DOWN; LEFT ]
    | 'F' -> [ DOWN; RIGHT ]
    | _ -> raise (Invalid_argument (String.make 1 pipe))
  in
  let locations = adjacent location in
  let valid_locations =
    List.filter
      (fun (direction, _) -> List.mem direction valid_directions)
      locations
  in
  List.map (fun (_, location) -> location) valid_locations

let rec traverse grid steps locations seen =
  let seen = List.map (fun location -> (location, steps)) locations @ seen in
  let next_locations =
    List.flatten (List.map (valid_adjacent grid) locations)
  in
  let next_locations =
    List.filter
      (fun location -> Option.is_none (List.assoc_opt location seen))
      next_locations
  in
  if List.length next_locations == 0 then seen
  else traverse grid (steps + 1) next_locations seen

let () =
  let grid = Aoc.Reader.read_grid () in
  let start, _ = List.find (fun (_, ch) -> ch == 'S') grid in
  let grid = (start, 'F') :: List.remove_assoc start grid in
  let distances = traverse grid 0 [ start ] [] in
  let values = List.map (fun (_, distance) -> distance) distances in
  let part1 = List.fold_left Int.max (List.hd values) (List.tl values) in
  Aoc.Answer.part1 6690 part1 string_of_int
