open Aoc.Point

let rec set_grid grid data =
  match data with
  | (p, x) :: xs ->
      Hashtbl.add grid p x;
      set_grid grid xs
  | [] -> ()

let get_max grid f =
  let values = Hashtbl.to_seq_keys grid |> Seq.map f |> List.of_seq in
  Aoc.Util.max values + 1

let find_rocks grid direction =
  let points =
    Hashtbl.to_seq grid
    |> Seq.filter (fun (_, ch) -> ch == 'O')
    |> Seq.map fst |> List.of_seq
  in
  match direction with
  | UP -> List.sort (fun a b -> Int.compare a.y b.y) points
  | DOWN -> List.sort (fun a b -> Int.compare b.y a.y) points
  | LEFT -> List.sort (fun a b -> Int.compare a.x b.x) points
  | RIGHT -> List.sort (fun a b -> Int.compare b.x a.x) points

let rec move_rock grid direction rock =
  let next =
    match direction with
    | UP -> { rock with y = rock.y - 1 }
    | DOWN -> { rock with y = rock.y + 1 }
    | LEFT -> { rock with x = rock.x - 1 }
    | RIGHT -> { rock with x = rock.x + 1 }
  in
  let can_move =
    match Hashtbl.find_opt grid next with
    | None -> false
    | Some value -> Char.equal '.' value
  in
  match can_move with
  | false -> ()
  | true ->
      Hashtbl.replace grid rock '.';
      Hashtbl.replace grid next 'O';
      move_rock grid direction next

let rec move_rocks grid direction rocks =
  match rocks with
  | [] -> ()
  | x :: xs ->
      move_rock grid direction x;
      move_rocks grid direction xs

let find_and_move grid direction =
  let rocks = find_rocks grid direction in
  move_rocks grid direction rocks

let get_load grid max_y =
  let rocks = find_rocks grid UP in
  Aoc.Util.sum (List.map (fun p -> max_y - p.y) rocks)

let run_cycle grid =
  find_and_move grid UP;
  find_and_move grid LEFT;
  find_and_move grid DOWN;
  find_and_move grid RIGHT

let grid_row grid xs y =
  let chars = List.map (fun x -> Hashtbl.find grid { x; y }) xs in
  String.of_seq (List.to_seq chars)

let grid_string grid max_x max_y =
  let xs = Seq.take max_x (Seq.ints 0) |> List.of_seq in
  let ys = Seq.take max_y (Seq.ints 0) |> List.of_seq in
  let rows = List.map (grid_row grid xs) ys in
  String.concat "\n" rows

let rec until_repeat grid max_x max_y seen =
  run_cycle grid;
  let as_string = grid_string grid max_x max_y in
  match List.assoc_opt as_string seen with
  | None ->
      let next = get_load grid max_y in
      until_repeat grid max_x max_y ((as_string, next) :: seen)
  | Some _ ->
      let result = List.rev seen in
      let preamble =
        Option.get
          (List.find_index (fun (x, _) -> String.equal x as_string) result)
      in
      let pattern = List.filteri (fun i _ -> i >= preamble) result in
      let pattern = List.map (fun (_, x) -> x) pattern in
      (preamble, pattern)

let () =
  let grid = Hashtbl.create 1000 in
  set_grid grid (Aoc.Reader.read_grid ());
  let max_x = get_max grid (fun p -> p.x) in
  let max_y = get_max grid (fun p -> p.y) in

  find_and_move grid UP;
  let part1 = get_load grid max_y in

  (* Complete the first cycle *)
  find_and_move grid LEFT;
  find_and_move grid DOWN;
  find_and_move grid RIGHT;

  let starting_seen = [ (grid_string grid max_x max_y, get_load grid max_y) ] in
  let preamble, pattern = until_repeat grid max_x max_y starting_seen in
  let pattern_index = (1000000000 - 1 - preamble) mod List.length pattern in
  let part2 = List.nth pattern pattern_index in
  Aoc.Answer.part1 109654 part1 string_of_int;
  Aoc.Answer.part2 94876 part2 string_of_int
